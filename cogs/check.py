import discord
import datetime
import asyncio
import os
import traceback
from discord import app_commands
from discord.ext import commands, tasks
import csv

class checkschedule(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.daily_reminder.start()

	time_to_repeat = [datetime.time(hour=7, minute=10, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8))), datetime.time(hour=7, minute=30, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8))), datetime.time(hour=7, minute=50, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))]
	
	@tasks.loop(time=time_to_repeat)
	async def daily_reminder(self):
		for time in self.time_to_repeat:
			if datetime.datetime.now().time() == time:
				await self.bot.get_channel(123456789012345678).send('This is a reminder.')
	


	@app_commands.command(name='checkschedule_alldates', description='查詢所有值日日子。')
	@app_commands.describe(class_='輸入班別，如5A請輸入A',grp_no='輸入組別，如組別1請輸入1')
	async def checkschedule_alldates(self, interaction: discord.Interaction, class_:str, grp_no:str):
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
		if int(grp_no) < 1 or int(grp_no) > 14:
			await interaction.followup.send('組別只可以係 0<x<15。')
			return
		await interaction.followup.send(f'你輸入嘅班別係{class_}，組別係{grp_no}。')
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
		
		await interaction.followup.send(f'你嘅組別係{grp_no}，你有{len(dong_zik_days)}次當值日。')
		total_string = ''
		for i in range(len(dong_zik_days)):
			total_string += f'{dong_zik_days[i]} - {dong_zik_classroomno[i]}\n'
		await interaction.followup.send('以下日子請當值:\n'+total_string)
	
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
		if int(grp_no) < 1 or int(grp_no) > 14:
			await interaction.followup.send('組別只可以係 0<x<15。')
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
	@app_commands.describe(class_='輸入班別，如5A請輸入A',grp_no='輸入組別，如組別1請輸入1',date='輸入日期，如01/01/2022請輸入01/01/2022')
	async def set_absent(self, interaction: discord.Interaction, class_:str, grp_no:str, date:str):
		file = open(f'5{class_}.csv', 'r')
		csv_reader = csv.reader(file)
		for row in csv_reader:
			if row[0] == 'Date':
				continue
			list22 = map(int,row[1].strip('][').split(', '))
			list22 = list(list22)
			if row[0] == date:
				if int(grp_no) in list22:
					list22.remove(int(grp_no))
					list22.append(int(grp_no)+1)
					row[1] = list22
					await interaction.followup.send(f'已經設定5{class_}班的{grp_no}組別在{date}缺席。')
					break
			await interaction.followup.send(f'該日組別{grp_no}無需當值。')
		file.close()
		file = open(f'5{class_}.csv', 'w',newline='')
		csv_writer = csv.writer(file)
		for row in csv_reader:
			csv_writer.writerow(row)
		file.close()
		await interaction.response.send_message(f'已經設定5{class_}班的{grp_no}組別缺席。')

				
async def setup(bot):
	await bot.add_cog(checkschedule(bot))
