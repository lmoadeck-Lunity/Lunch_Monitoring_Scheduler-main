import discord, time, os, asyncio, traceback
from discord.ext import commands
from dotenv import load_dotenv

# load_dotenv('./Stepfordle/.env')
load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=',<', intents=intents)
admin = int(os.getenv('ADMIN'))

@bot.event
async def on_ready():
	print('Stepfordle is ready.')
	print(f'System time: {time.ctime()}')

@bot.event
async def on_message(message):
	await bot.process_commands(message)

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

async def main():
	async with bot:
		await bot.start(os.getenv('TOKEN_TEMP'))

if __name__ == '__main__':
	asyncio.run(main())