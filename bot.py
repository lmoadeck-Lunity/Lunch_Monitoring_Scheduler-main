import discord, time, os, asyncio, traceback
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import datetime
import calendar
from dateutil.rrule import *
from dateutil.parser import *
import csv

from datetime import *
import itertools
# load_dotenv('./Stepfordle/.env')
load_dotenv()

defIntents = discord.Intents.default()
defIntents.members = True
defIntents.message_content = True

bot = commands.Bot(command_prefix=';', intents=defIntents)
admin = int(os.getenv('ADMIN'))

@bot.event
async def on_ready():
	print('Rice is ready.')
	print(f'System time: {time.ctime()}')
	await bot.load_extension(f'cogs.check')


@bot.event
async def on_message(message):
	await bot.process_commands(message)
	# print(f'{message.author} sent a message at {time.ctime()}: {message.content}')

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
				datetime_start = date(2024, st_month, st_day) if st_month > 6 else date(2025, st_month, st_day)
				datetime_end = date(2024, en_month, en_day) if en_month > 6 else date(2025, en_month, en_day)
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
		dates_range = list(rrule(freq=DAILY, until=datetime(2025, 6, 30), dtstart=datetime(2024, 9, 4)))
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
		print(A, B, C, D)
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
		file2 = open('')
@bot.command()
async def send_absent_list(ctx):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	else:
		file = file.open('total_absentees.csv', 'r')
		await ctx.send(f'```csv\n{file.read()}```')
		file.close()
@bot.command()
async def revoke_absent(ctx,index:int):
	if ctx.author.id != admin: 
		await ctx.send('You do not have permission to use this command.')
		return
	else:
		file = open('total_absentees.csv', 'r')
		lines = file.readlines()
		file.close()
		file = open('total_absentees.csv', 'w')
		lines.pop(index)
		file.writelines(lines)
		file.close()
		await ctx.send('Revoked absence.')
async def main():
	async with bot:
		await bot.start(os.getenv('TOKEN_TEMP'))




if __name__ == '__main__':
	asyncio.run(main())