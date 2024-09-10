import discord, time, os, asyncio, traceback
from discord.ext import commands
from dotenv import load_dotenv


import datetime
import calendar
from dateutil.rrule import *
from dateutil.parser import *
import csv
import itertools
# load_dotenv('./Stepfordle/.env')
load_dotenv()

defIntents = discord.Intents.default()
defIntents.members = True
defIntents.message_content = True
global channel_map
channel_map = {
	'A': 1280752582050054167,
	'B': 1280752596516208720,
	'C': 1280752611783479336,
	'D': 1280752621954797568
}
bot = commands.Bot(command_prefix=';', intents=defIntents)
admin = int(os.getenv('ADMIN'))
def set_absent(class_:str, grp_no:str, month:int, day:int):
		# global max_gp
		max_gp = {'A':15,'B':14,'C':8,'D':8}
		# global classroom_lookup_table
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
		date = f'{str(day).zfill(2)}/{str(month).zfill(2)}/{2024 if month > 6 else 2025}'
		if class_ not in ['A','B','C','D']:
			print('班別只可以係 A, B, C, D。')
			return
		if int(grp_no) < 1 or int(grp_no) > 15:
			print('組別只可以係 0<x<16。')
			return
		if datetime.datetime.strptime(date, '%d/%m/%Y').date() < datetime.datetime.now().date():
			print('日期唔可以係過去。')
			return
		if datetime.datetime.strptime(date, '%d/%m/%Y').date() > datetime.datetime(2025, 6, 30).date():
			print ('日期超過全日制學期上課日終止點。')
			return
		if datetime.datetime.strptime(date, '%d/%m/%Y').date().weekday() > 4:
			print('日期唔可以係星期六或星期日。')
			return
		if int(grp_no) > max_gp[class_]:
			print('組別唔可以超過班別組別數量。')
			return
		
		found1 = False
		runtimes = 0
		moved = False
		if class_ in ['C','D']:
			print('抱歉，班別C和D唔支援呢個功能。')
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
						index_of_gp = list22.index(int(grp_no))
						print('index_of_gp', index_of_gp)
						# print('1', list22)
						# list22.append((max(list22)+1 if max(list22) < max_gp[class_] else list22[-1]+1))
						list22[index_of_gp] = max(list22)+1 if max(list22) < max_gp[class_] else list22[-1]+1
						# print('2', list22)
						csv_reader[runtimes][1] = list22
						# print(csv_reader[runtimes][1])
						# print(csv_reader)
						moved = True
						continue
					else:
						print(f'該日組別{grp_no}無需當值。')
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
				print(f'該日組別{grp_no}無需當值。')
				return
			if success:
				print(f'已經設定5{class_}班的{grp_no}組別在{date}缺席，並且已將所有組別編號移向後一格。')
				
			file.close()
			file = open(f'5{class_}.csv', 'w',newline='')
			csv_writer = csv.writer(file)
			for row in csv_reader:
				csv_writer.writerow(row)
			file.close()
			print(f'成功更新時間表。')
			return

@bot.event
async def on_ready():
	print('Rice is ready.')
	print(f'System time: {time.ctime()}')
	await bot.load_extension(f'cogs.check')

	try:
		file = open('total_absentees.csv', 'r')
		csv_reader = csv.reader(file)
		for line in csv_reader:
			if line == []: 
				continue
			
			class_ = line[0].strip('5')
			grp_no = line[1]
			date = line[2]
			set_absent(class_, grp_no, int(date.split('/')[1]), int(date.split('/')[0]))
		file.close()
		print('Loaded absentees.')
	except Exception as e:
		traceback.print_exception(type(e), e, e.__traceback__)
		print('Failed to load absentees.')
		file.close()
	


@bot.event
async def on_message(message):
	await bot.process_commands(message)
	print(f'{message.author} sent a message at {time.ctime()}: {message.content}')

@bot.command()
async def cog_load(ctx, cog_name = None):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	if not cog_name:
		for filename in os.listdir('./cogs'):	
			await bot.load_extension(f'cogs.{filename[:-3]}')
			await ctx.send(f'Loaded cog `{filename[:-3]}`.')
			print(f'Loaded cog {filename[:-3]} at {time.ctime()}.')
	else:
		try:
			await bot.load_extension(f'cogs.{cog_name}')
		except Exception as e:
			await ctx.send(f'Failed to load `{cog_name}`.')
			traceback.print_exception(type(e), e, e.__traceback__)
		else:
			await ctx.send(f'Loaded cog `{cog_name}`.')
			print(f'Loaded cog {cog_name} at {time.ctime()}.')

@bot.command()
async def cog_unload(ctx, cog_name = None):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	if not cog_name:
		await ctx.send('Please specify a cog to unload.')
	else:
		try:
			await bot.unload_extension(f'cogs.{cog_name}')
		except Exception as e:
			await ctx.send(f'Failed to unload `{cog_name}`.')
			traceback.print_exception(type(e), e, e.__traceback__)
		else:
			await ctx.send(f'Unloaded cog `{cog_name}`.')
			print(f'Unloaded cog {cog_name} at {time.ctime()}.')

@bot.command()
async def cog_reload(ctx, cog_name:str = None):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	if not cog_name:
		await ctx.send('Please specify a cog to reload.')
	else:
		try:
			await bot.reload_extension(f'cogs.{cog_name}')
		except Exception as e:
			await ctx.send(f'Failed to reload `{cog_name}`.')
			traceback.print_exception(type(e), e, e.__traceback__)
		else:
			await ctx.send(f'Reloaded cog `{cog_name}`.')
			print(f'Reloaded cog {cog_name} at {time.ctime()}.')

@bot.command()
async def smclear(ctx):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	try: 
		cleared_commands = bot.tree.clear_commands(guild=None)
	except Exception as e: 
		await ctx.send('An error has occurred during the clearing of slash commands.')
		traceback.print_exception(type(e), e, e.__traceback__)
	else: 
		await ctx.send(f'Cleared {len(cleared_commands)} command(s).')

@bot.command()
async def smsync(ctx):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	print('Syncing commands...')
	try: 
		synced_commands = await bot.tree.sync()
	except Exception as e: 
		await ctx.send('An error has occurred during the syncing of slash commands.')
		traceback.print_exception(type(e), e, e.__traceback__)
	else: 
		await ctx.send(f'Synced {len(synced_commands)} command(s).')
@bot.command()
async def machine_time(ctx):
	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	await ctx.send(str(current_time))

@bot.command()
async def reset_timetable(ctx):
	try:
		if ctx.author.id != admin: 
			await ctx.send('You do not have permission to use this command.')
			return
		else:
			parserinfo_ = parserinfo(dayfirst=True)

			def parse_date(date_str):
				if '-' in date_str:
					start, end = date_str.split('-')
					st_day, st_month = map(int, start.split('/'))
					en_day, en_month = map(int, end.split('/'))
					# print(st_day, st_month, en_day, en_month)
					datetime_start = datetime.date(2024, st_month, st_day) if st_month > 6 else datetime.date(2025, st_month, st_day)
					datetime_end = datetime.date(2024, en_month, en_day) if en_month > 6 else datetime.date(2025, en_month, en_day)
					return list(rrule(freq=DAILY, until=datetime_end, dtstart=datetime_start))
				else:
					return parse(date_str,parserinfo=parserinfo_)
			calendar_ = calendar.Calendar()
			holidays = '18/9,27/9,1/10,4/10,11/10,16/10-24/10,4/11,19/11,20/11,2/12,20/12,22/12-2/1,6/1,20/1,27/1-5/2,19/3,4/4-24/4,1/5,5/5,13/5,26/5,5/6,23/6'.split(',')
			holidays = [parse_date(x) for x in holidays]
			holidays = list(itertools.chain([a for x in holidays if isinstance(x, list) for a in x], [x for x in holidays if not isinstance(x, list)]))
			# print(holidays)
			A = []
			B = []
			C = []
			D = []
			count = 0
			dates_range = list(rrule(freq=DAILY, until=datetime.datetime(2025, 6, 30), dtstart=datetime.datetime(2024, 9, 4)))
			dates_range = [x for x in dates_range if x.weekday() < 5 and x not in holidays]
			for date in dates_range:
				if date.weekday() == 0:
					A.append(date)
				elif date.weekday() == 1:
					B.append(date)
				elif date.weekday() == 2:
					C.append(date)
				elif date.weekday() == 3:
					D.append(date)
				elif date.weekday() == 4:
					if count % 4 == 0:
						A.append(date)
					elif count % 4 == 1:
						B.append(date)
					elif count % 4 == 2:
						C.append(date)
					elif count % 4 == 3:
						D.append(date)
					count += 1
			# print(A, B, C, D)
			temparray = []
			count = 0
			for i in range(4):
				csv_file = open(f'5{chr(65+i)}.csv', 'w',newline='')
				csv_writer = csv.writer(csv_file)
				csv_writer.writerow(['Date','Groups'])

				for date in list(A) if i == 0 else list(B) if i == 1 else list(C) if i == 2 else list(D):
					while len(temparray) < 8:
						temparray.append((count%15+1) if i == 0 else (count%14+1) if i == 1 else (count%8+1) if i == 2 else (count%8+1))
						count +=1
					csv_writer.writerow([date.strftime('%d/%m/%Y'), temparray])
					temparray = []
				csv_file.close()
			
			await ctx.send('Timetable reset.')
	except Exception as e:
		traceback.print_exception(type(e), e, e.__traceback__)
		await ctx.send('An error has occurred.')

@bot.command()
async def send_absent_list(ctx):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	else:
		try:
			file = open('total_absentees.csv', 'r')
			await ctx.send(f'```csv\n{file.read()}```')
			file.close()
		except Exception as e:
			traceback.print_exception(type(e), e, e.__traceback__)
			await ctx.send('An error has occurred.')

@bot.command()
async def revoke_absent(ctx,index:int):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	else:
		try:
			file = open('total_absentees.csv', 'r')
			lines = file.readlines()
			file.close()
			file = open('total_absentees.csv', 'w')
			lines.pop(index)
			file.writelines(lines)
			file.close()
			await ctx.send('Revoked absence.')
		except Exception as e:
			traceback.print_exception(type(e), e, e.__traceback__)
			await ctx.send('An error has occurred.')
@bot.command()
async def cleanup(self):
		for i in ['A','B','C','D']:
			channel = self.bot.get_channel(channel_map[i])
			async for line in channel.history(limit=None):
				await line.delete()
		return

async def main():
	async with bot:
		await bot.start(os.getenv('TOKEN_TEMP'))




if __name__ == '__main__':
	try:
		asyncio.run(main())
	except Exception as e:
		traceback.print_exception(type(e), e, e.__traceback__)
		print('An error has occurred.')