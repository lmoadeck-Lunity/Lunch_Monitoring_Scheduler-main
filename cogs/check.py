import discord
import datetime
import asyncio
import os
import traceback
from discord import app_commands
from discord.ext import commands, tasks
import csv

global max_gp
max_gp = {'A':15,'B':14,'C':8,'D':8}
global classroom_lookup_table
classroom_lookup_table = {
		1 : '101 - 1A',
		2 : '102 - 1B',
		3 : '103 - 1C',
		4 : '104 - 1D',
		5 : '201 - 2A',
		6 : '202 - 2B',
		7 : '203 - 2C',
		8 : '204 - 2D',
}
global role_map
global channel_map
channel_map = {
	'A': 1280752582050054167,
	'B': 1280752596516208720,
	'C': 1280752611783479336,
	'D': 1280752621954797568
}
role_map = {
	1: 894801198874505256,
	2: 894801275974197299,
	3: 894801299177087037,
	4: 894801299495870494,
	5: 894801301597200404,
	6: 894801302608023552,
	7: 894801303455301683,
	8: 894801304113786900,
	9: 894801304394817557,
	10: 894801304759709697,
	11: 894801304805867531,
	12: 894801306206744577,
	13: 894801306517114890,
	14: 894801307066585118,
	15: 894801307775430656
}
class checkschedule(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.daily_reminder.start()
		self.after_lunchtime_cleanup.start()

	time_to_repeat = [datetime.time(hour=7, minute=10, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8))), datetime.time(hour=7, minute=30, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8))), datetime.time(hour=7, minute=50, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))]
	after_lunchtime = datetime.time(hour=13, minute=0, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
	@tasks.loop(time=time_to_repeat)
	async def daily_reminder(self):
		print(datetime.datetime.now().time())
		print('Sending reminder')
		if datetime.datetime.now().weekday() == 6 or datetime.datetime.now().weekday() == 5:
			return
		guild_id = 889143681402167306
		#5A 1280752582050054167
		#5B 1280752596516208720
		#5C 1280752611783479336
		#5D 1280752621954797568
		# 		@Client.command(pass_context = True)
		# async def clear(ctx, number):
		#     number = int(number) #Converting the amount of messages to delete to an integer
		#     counter = 0
		#     async for x in Client.logs_from(ctx.message.channel, limit = number):
		#         if counter < number:
		#             await Client.delete_message(x)
		#             counter += 1
		#             await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even
		try:
			for i in ['A','B','C','D']:
				file = open(f'5{i}.csv', 'r')
				csv_reader = csv.reader(file)
				channel = self.bot.get_channel(channel_map[i])

				for line in csv_reader:
					if line[0] == 'Date':
						continue
					list22 = map(int,line[1].strip('][').split(', '))
					list22 = list(list22)
					channel = self.bot.get_channel(channel_map[i])
					if datetime.datetime.now().date() == datetime.datetime.strptime(f'{line[0]}/00:00', '%d/%m/%Y/%H:%M').date():
						async for line in channel.history(limit=None):
							await line.delete()
						await channel.send(f'是日更表為：')
						for index, value in enumerate(list22,1):
							await channel.send(f'第{value}組 1230 --> {classroom_lookup_table[index]} ||<@&{role_map[index]}>||')	
		except Exception as e:
			print(e)
			traceback.print_exc()
		return
	@tasks.loop(time=after_lunchtime)
	async def after_lunchtime_cleanup(self):
		for i in ['A','B','C','D']:
			FILENAME = f'5{i}.csv'
			DELETE_LINE_NUMBER = 1
			channel = self.bot.get_channel(channel_map[i])
			async for line in channel.history(limit=None):
				await line.delete()
			with open(FILENAME) as f:
				data = f.read().splitlines() # Read csv file
			with open(FILENAME, 'w') as g:
				g.write('\n'.join([data[:DELETE_LINE_NUMBER]] + data[DELETE_LINE_NUMBER+1:])) # Write to file without the first line
		return


					

	


	@app_commands.command(name='checkschedule_alldates', description='查詢所有值日日子。')
	@app_commands.describe(class_='輸入班別，如5A請輸入A',grp_no='輸入組別，如組別1請輸入1')
	async def checkschedule_alldates(self, interaction: discord.Interaction, class_:str, grp_no:str):
		await interaction.response.defer()
		dong_zik_days = []
		dong_zik_classroomno = []
		
		if class_ not in ['A','B','C','D']:
			await interaction.followup.send('班別只可以係 A, B, C, D。')
			return
		if int(grp_no) < 1 or int(grp_no) > 15:
			await interaction.followup.send('組別只可以係 0<x<16')
			return
		if int(grp_no) > max_gp[class_]:
			await interaction.followup.send('組別唔可以超過班別組別數量。')
			return
		# await interaction.followup.send(f'你輸入嘅班別係{class_}，組別係{grp_no}。')
		file = open(f'5{class_}.csv', 'r')
		csv_reader = csv.reader(file)
		for line in csv_reader:
			if line[0] == 'Date':
				continue
			list22 = map(int,line[1].strip('][').split(', '))
			list22 = list(list22)
			# await interaction.followup.send(list22)
			if int(grp_no) in list22:
				dong_zik_days.append(line[0])
				dong_zik_classroomno.append(classroom_lookup_table[list22.index(int(grp_no))+1])
		
		# await interaction.followup.send(f'你嘅組別係{grp_no}，你有{len(dong_zik_days)}次當值日。')
		total_string = ''
		for i in range(len(dong_zik_days)):
			if class_ in ['A','B']:
				total_string += f'{dong_zik_days[i]} - {dong_zik_classroomno[i]}\n'
			else:
				total_string += f'{dong_zik_days[i]}\n'
		await interaction.followup.send(f'你輸入嘅班別係{class_}，組別係{grp_no}。\n你有{len(dong_zik_days)}次當值日。\n以下日子請當值:\n--------------------------\n'+total_string)
	
	@app_commands.command(name='checkschedule_nextdate', description='查詢下一次值日日子。')
	@app_commands.describe(class_='輸入班別，如5A請輸入A',grp_no='輸入組別，如組別1請輸入1')
	async def checkschedule_nextdate(self, interaction: discord.Interaction, class_:str, grp_no:str):
		await interaction.response.defer()
		# print('checkschedule_nextdate')
		classroom_lookup_table = {
		1 : '101 - 1A',
		2 : '102 - 1B',
		3 : '103 - 1C',
		4 : '104 - 1D',
		5 : '201 - 2A',
		6 : '202 - 2B',
		7 : '203 - 2C',
		8 : '204 - 2D',
		}
		dong_zik_days = []
		dong_zik_classroomno = []
		
		if class_ not in ['A','B','C','D']:
			await interaction.followup.send('班別只可以係 A, B, C, D。')
			return
		if int(grp_no) < 1 or int(grp_no) > 15:
			await interaction.followup.send('組別只可以係 0<x<16。')
			return
		if int(grp_no) > max_gp[class_]:
			await interaction.followup.send('組別唔可以超過班別組別數量。')
			return
		# await interaction.followup.send(f'你輸入嘅班別係{class_}，組別係{grp_no}。')
		file = open(f'5{class_}.csv', 'r')
		csv_reader = csv.reader(file)
		for line in csv_reader:
			if line[0] == 'Date':
				continue
			list22 = map(int,line[1].strip('][').split(', '))
			list22 = list(list22)
			# await interaction.followup.send(list22)
			if int(grp_no) in list22:
				if datetime.datetime.now().date() > datetime.datetime.strptime(f'{line[0]}/00:00', '%d/%m/%Y/%H:%M').date():
					continue
				dong_zik_days.append(line[0])
				dong_zik_classroomno.append(classroom_lookup_table[list22.index(int(grp_no))+1])
		
		if len(dong_zik_days) == 0:
			await interaction.followup.send('你嘅組別係{grp_no}，你冇當值日。')
			return
		# await interaction.followup.send(f'你嘅組別係{grp_no}，你有{len(dong_zik_days)}次當值日。')
		if datetime.datetime.now().date() > datetime.datetime.strptime(f'{dong_zik_days[-1]}/00:00', '%d/%m/%Y/%H:%M').date():
			await interaction.followup.send('本年度已經冇更多值日。多謝您這一年的付出。中六見。')
			return
		# await interaction.followup.send(f'你嘅組別係{grp_no}，你有{len(dong_zik_days)}次當值日。')
		substring1 = f'，地點係{dong_zik_classroomno[0]}。'
		substring2 = f'。'
		await interaction.followup.send(f'你下一次當值日係{dong_zik_days[0]}{substring1 if class_ not in ['C','D'] else substring2}')

	@app_commands.command(name='set_absent', description='設定缺席。')
	@app_commands.describe(class_='輸入班別，如5A請輸入A',grp_no='輸入組別，如組別1請輸入1',month = '輸入月份，如9月請輸入9',day = '輸入日期，如17號請輸入17')
	async def set_absent(self, interaction: discord.Interaction, class_:str, grp_no:str, month:int, day:int):
		await interaction.response.defer()
		date = f'{str(day).zfill(2)}/{str(month).zfill(2)}/{2024 if month > 6 else 2025}'
		if class_ not in ['A','B','C','D']:
			await interaction.followup.send('班別只可以係 A, B, C, D。')
			return
		if int(grp_no) < 1 or int(grp_no) > 15:
			await interaction.followup.send('組別只可以係 0<x<16。')
			return
		if datetime.datetime.strptime(date, '%d/%m/%Y').date() < datetime.datetime.now().date():
			await interaction.followup.send('日期唔可以係過去。')
			return
		if datetime.datetime.strptime(date, '%d/%m/%Y').date() > datetime.datetime(2025, 6, 30).date():
			await interaction.followup.send('日期超過全日制學期上課日終止點。')
			return
		if datetime.datetime.strptime(date, '%d/%m/%Y').date().weekday() > 4:
			await interaction.followup.send('日期唔可以係星期六或星期日。')
			return
		if int(grp_no) > max_gp[class_]:
			await interaction.followup.send('組別唔可以超過班別組別數量。')
			return
		
		found1 = False
		runtimes = 0
		moved = False
		if class_ in ['C','D']:
			await interaction.followup.send('抱歉，班別C和D唔支援呢個功能。')
		else:
			file = open(f'5{class_}.csv', 'r')
			csv_reader = list(csv.reader(file))
			for row in csv_reader:



				if row[0] == 'Date':
					continue
				runtimes += 1
				list22 = map(int,row[1].strip('[]').split(', '))
				list22 = list(list22)
				
				if row[0] == date:
					# print('found')
					found1 = True
					if int(grp_no) in list22:
						# print('found2', list22)
						# print('0', runtimes)
						list22.remove(int(grp_no))
						# print('1', list22)
						list22.append((max(list22)+1 if max(list22) < max_gp[class_] else list22[-1]+1))
						# print('2', list22)
						csv_reader[runtimes][1] = list22
						# print(csv_reader[runtimes][1])
						# print(csv_reader)
						moved = True
						
						continue
					else:
						await interaction.followup.send(f'該日組別{grp_no}無需當值。')
						return
				if moved:
					# print('moved')
					list22 = [x+1 if x < max_gp[class_] else 1 for x in list22]
					csv_reader[runtimes][1] = list22
					# print(runtimes)
					# print(csv_reader)
					success = True
				# print('3',found1)
			# print('4',found1)
			
			if not found1:
				await interaction.followup.send(f'該日組別{grp_no}無需當值。')
				return
			if success:
				await interaction.followup.send(f'已經設定5{class_}班的{grp_no}組別在{date}缺席，並且已將所有組別編號移向後一格。')
				
			file.close()
			file = open(f'5{class_}.csv', 'w',newline='')
			csv_writer = csv.writer(file)
			for row in csv_reader:
				csv_writer.writerow(row)
			file.close()
			await interaction.followup.send(f'成功更新時間表。')
			return
		
	@app_commands.command(name='check_today', description='查詢今日值日。')
	@app_commands.describe()
	async def check_today(self, interaction: discord.Interaction):
		await interaction.response.defer()
		total_string = ''
		for i in ['A','B','C','D']:
			file = open(f'5{i}.csv', 'r')
			csv_reader = csv.reader(file)
			
			for line in csv_reader:
				if line[0] == 'Date':
					continue
				list22 = map(int,line[1].strip('][').split(', '))
				list22 = list(list22)
				if datetime.datetime.now().date() == datetime.datetime.strptime(f'{line[0]}/00:00', '%d/%m/%Y/%H:%M').date():
					await interaction.followup.send(f'是日更表為：')
					for index, value in enumerate(list22):
						total_string +=f'5{i}班 第{value}組 -> {classroom_lookup_table[index+1]}'+'\n'
		await interaction.followup.send(total_string)
		return
	@app_commands.command(name='check_day', description='查詢指定日期值日。')
	@app_commands.describe(month='輸入月份，如9月請輸入9',day='輸入日期，如17號請輸入17')
	async def check_day(self, interaction: discord.Interaction, month:int, day:int):
		date = f'{str(day).zfill(2)}/{str(month).zfill(2)}/{2024 if month > 6 else 2025}'
		await interaction.response.defer()
		total_string = ''
		for i in ['A','B','C','D']:
			file = open(f'5{i}.csv', 'r')
			csv_reader = csv.reader(file)
			
			for line in csv_reader:
				if line[0] == 'Date':
					continue
				list22 = map(int,line[1].strip('][').split(', '))
				list22 = list(list22)
				if datetime.datetime.strptime(date, '%d/%m/%Y').date() == datetime.datetime.strptime(f'{line[0]}/00:00', '%d/%m/%Y/%H:%M').date():
					await interaction.followup.send(f'是日更表為：')
					for index, value in enumerate(list22):
						total_string +=f'5{i}班 第{value}組 -> {classroom_lookup_table[index+1]}'+'\n'
		await interaction.followup.send(total_string)
		return
						
					
		


				
async def setup(bot):
	await bot.add_cog(checkschedule(bot))
