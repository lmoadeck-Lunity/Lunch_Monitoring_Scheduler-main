import discord
import datetime
import asyncio
import os
import traceback
from discord import app_commands
from discord.ext import commands, tasks
import csv

global max_gp
max_gp = {'A':15,'B':14,'C':14,'D':11}
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
class checkschedule(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.daily_reminder.start()

	time_to_repeat = [datetime.time(hour=7, minute=10, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8))), datetime.time(hour=7, minute=30, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8))), datetime.time(hour=7, minute=50, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))]
	after_lunchtime = datetime.time(hour=13, minute=0, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
	@tasks.loop(time=time_to_repeat)
	async def daily_reminder(self):
		sanity_check_map = {
			'A': 1280752582050054167,
			'B': 1280752596516208720,
			'C': 1280752611783479336,
			'D': 1280752621954797568
		}
		

		print(datetime.datetime.now().time())
		print('Sending reminder')

		guild_id = 889143681402167306
		#5A 1280752582050054167
		#5B 1280752596516208720
		#5C 1280752611783479336
		#5D 1280752621954797568
		for i in ['A','B','C','D']:
			file = open(f'5{i}.csv', 'r')
			csv_reader = csv.reader(file)
			
			for line in csv_reader:
				if line[0] == 'Date':
					continue
				list22 = map(int,line[1].strip('][').split(', '))
				list22 = list(list22)
				channel = self.bot.get_channel(sanity_check_map[i])
				if datetime.datetime.now().date() == datetime.datetime.strptime(f'{line[0]}/00:00', '%d/%m/%Y/%H:%M').date():
					await channel.send(f'是日更表為：')
					for index, value in enumerate(list22):
						await channel.send(f'第{value}組 1230 私 {classroom_lookup_table[index+1]} ||@G{value}||')	
	@tasks.loop(time=after_lunchtime)
	async def after_lunchtime_cleanup(self):
		for i in ['A','B','C','D']:
			FILENAME = f'5{i}.csv'
			DELETE_LINE_NUMBER = 1

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
		if grp_no > max_gp[class_]:
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
			total_string += f'{dong_zik_days[i]} - {dong_zik_classroomno[i]}\n'
		await interaction.followup.send(f'你輸入嘅班別係{class_}，組別係{grp_no}。\n你有{len(dong_zik_days)}次當值日。\n以下日子請當值:\n--------------------------\n'+total_string)
	
	@app_commands.command(name='checkschedule_nextdate', description='查詢下一次值日日子。')
	@app_commands.describe(class_='輸入班別，如5A請輸入A',grp_no='輸入組別，如組別1請輸入1')
	async def checkschedule_nextdate(self, interaction: discord.Interaction, class_:str, grp_no:str):
		await interaction.response.defer()
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
		if grp_no > max_gp[class_]:
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
		
		await interaction.followup.send(f'你下一次當值日係{dong_zik_days[0]}，地點係{dong_zik_classroomno[0]}。')

	@app_commands.command(name='set_absent', description='設定缺席。')
	@app_commands.describe(class_='輸入班別，如5A請輸入A',grp_no='輸入組別，如組別1請輸入1',date='輸入日期，如2024年9月17日請輸入17/09/2024')
	async def set_absent(self, interaction: discord.Interaction, class_:str, grp_no:str, date:str):
		await interaction.response.defer()
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
		if grp_no > max_gp[class_]:
			await interaction.followup.send('組別唔可以超過班別組別數量。')
			return
		
		found1 = False
		runtimes = 0
		file = open(f'5{class_}.csv', 'r')
		csv_reader = list(csv.reader(file))
		moved = False
		for row in csv_reader:
			if row[0] == 'Date':
				continue
			runtimes += 1
			list22 = map(int,row[1].strip('][').split(', '))
			list22 = list(list22)
			found1 = False
			if row[0] == date:
				found1 = True
				if int(grp_no) in list22:
					list22.remove(int(grp_no))
					list22.append(max(list22)+1)

					csv_reader[runtimes][1] = list22
					moved = True


					continue
			if moved:
				# increment all numbers in the list by 1 if they are less than 14, otherwise set them to 1
				list22 = [x+1 if x < max_gp[class_] else 1 for x in list22]
				csv_reader[runtimes][1] = list22
				await interaction.followup.send(f'已經設定5{class_}班的{grp_no}組別在{date}缺席，並且已將所有組別編號移向後一格。')

		if not found1:
			await interaction.followup.send(f'該日組別{grp_no}無需當值。')
			return
			
		file.close()
		file = open(f'5{class_}.csv', 'w',newline='')
		csv_writer = csv.writer(file)
		for row in csv_reader:
			csv_writer.writerow(row)
		file.close()
		await interaction.followup.send(f'成功更新時間表。')
		return

				
async def setup(bot):
	await bot.add_cog(checkschedule(bot))
