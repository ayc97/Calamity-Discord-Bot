import discord, typing, random
from discord.ext import commands
from pathlib import Path
from dateutil import parser
from pytz import timezone

intents = discord.Intents.default()
intents.members = True

activity = discord.Game(name="!help")
bot = commands.Bot('!', intents=intents, activity=activity)
token = Path('token.txt').read_text()

@bot.event
async def on_ready():
    print('Bot is online')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.command(
    name = 'raid',
    description = 'Sets a channel wide notification for a raid date.',
    usage = '<DD/MM/YY> <XXXX> <±HH>\nE.g: !raid 01/12/21 2230 +08'
)
async def raid(ctx, *, date: str):
    parsedDate = parser.parse(date)
    parsedDateUTC = parsedDate.astimezone(timezone('UTC')).strftime("%a %d %b %H:%M UTC")
    raidDateSG = parsedDate.astimezone(timezone('Singapore')).strftime("%a %d %b %H:%M SGT")
    raidDateNYC = parsedDate.astimezone(timezone('America/New_York')).strftime("%a %d %b %H:%M EDT")
    msg = await ctx.send(f'@here **Raid is set for:**\n{raidDateSG}\n{parsedDateUTC}\n{raidDateNYC}\n\nReact with \U0001F44D or \U0001F44E')
    await msg.add_reaction("\U0001F44D")
    await msg.add_reaction("\U0001F44E")
    return

@bot.command(
    name = 'roll',
    description = 'Rolls a random number from X to Y.',
    usage = 'X Y'
)
async def roll(ctx, min: int, max: int):
    return await ctx.send(str(random.randint(min,max)))

@bot.command(
    name = 'uptime',
    description = 'Calculates an approximate uptime given the Boss, DPM, and TTK',
    usage = '<Emp/VL/Kerb> <DPM in billions> <TTK in seconds>\nE.g: !uptime vonleon 300 1500'
)
async def uptime(ctx, boss: str, dpm: float, ttk: float):
    ttkMinutes = ttk/60
    maxDPM = dpm*ttkMinutes

    if ('emp' in boss.lower() or 'cyg' in boss.lower()):
        empUptime = (27820/maxDPM)*100
        return await ctx.send('Uptime for Empress was: ' + "%.2f" % empUptime +'%')
    
    if ('v2' in boss.lower()):
        v2Uptime = (17195/maxDPM)*100
        return await ctx.send('Uptime for V2 was: ' + "%.2f" % v2Uptime +'%')

    if ('von' in boss.lower() or 'vl' in boss.lower()):
        vlUptime = (5250/maxDPM)*100
        return await ctx.send('Uptime for Von Leon was: ' + "%.2f" % vlUptime +'%')

    if 'kerb' in boss.lower():
        kerbUptime = (3500/maxDPM)*100
        return await ctx.send('Uptime for Kerberos was: ' + "%.2f" % kerbUptime +'%')

    return await ctx.send('Something went wrong. Please check your input.')

bot.run(token)
