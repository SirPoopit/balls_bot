import discord
from discord.ext import commands
from collections import defaultdict
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
balls_counter = defaultdict(int)
log_file_path = '/balls_bot/balls_log.txt'

def read_log_and_tally():
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            next(f)  # Skip header line
            for line in f:
                user, count = line.strip().split(', ')
                balls_counter[user] += int(count)

@bot.event
async def on_ready():
    read_log_and_tally()
    print(f'{bot.user} ready to ball')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'balls' in message.content.lower() and not message.content.startswith('!'):
        await message.channel.send('balls')
        
        user_id = str(message.author.id)
        balls_counter[user_id] += 1
        
        with open(log_file_path, 'a') as f:
            f.write(f'{message.author}, {balls_counter[user_id]}\n')
        
    await bot.process_commands(message)

@bot.command(name='topballs', aliases=['top', 'ballers', 'topballers'])
async def top_balls(ctx, n: int = 3):
    top_3_users = sorted(balls_counter.items(), key=lambda item: item[1], reverse=True)[:n]
    top_3_mentions = [f'<@{user_id}>' for user_id, count in top_3_users]
    response = f'# Top {n} ballers:\n' + '\n'.join([f'{mention}: {count}' for mention, (user_id, count) in zip(top_3_mentions, top_3_users)])
    await ctx.send(response)

@bot.command(name='BALLS')
async def send_log(ctx):
    await ctx.author.send(file=discord.File(log_file_path))

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('MTI2MDI0OTE0Njc2NjY1NTUwOQ.GEHbsE.8SxhrzQ4UyVspw06apYlCr2ls-voHsUbGdxNSU')
