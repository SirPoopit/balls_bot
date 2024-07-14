import discord
from discord.ext import commands
from collections import defaultdict
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
balls_counter = defaultdict(int)
log_directory = 'balls_bot'
balls_counter = {}

# Dictionary to keep track of the number of times each user has said "balls" per server
balls_counter = defaultdict(lambda: defaultdict(int))

def get_log_file_path(guild_id):
    return os.path.join(log_directory, f'balls_log_{guild_id}.txt')

def read_log_and_tally(guild_id):
    log_file_path = get_log_file_path(guild_id)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            next(f)  # Skip header line
            for line in f:
                try:
                    user, count = line.strip().split(', ')
                    balls_counter[guild_id][user] += int(count)
                except ValueError:
                    continue
                    
@bot.event
async def on_ready():
    for guild in bot.guilds:
        guild_id = guild.id
        balls_counter[guild_id] = {}
        read_log_and_tally(guild_id)
    print(f'{bot.user} ready to ball')

@bot.event
async def on_message(message):
    if message.author == bot.user or message.content.startswith('!'):
        return    
        
    guild_id = message.guild.id
    
    # Check if message contains 'balls' and does not start with '!'
    if 'balls' in message.content.lower():
        await message.channel.send('balls')
        
        # Update the counter for the user
        user_id = str(message.author.id)
        if user_id not in balls_counter[guild_id]:
            balls_counter[guild_id][user_id] = 0
        balls_counter[guild_id][user_id] += 1

        
        log_file_path = get_log_file_path(guild_id)       
        with open(log_file_path, 'a') as f:
            f.write(f'{message.author}, {balls_counter[guild_id][user_id]}\n')
        
    await bot.process_commands(message)

@bot.command(name='topballs', aliases=['top', 'ballers', 'topballers'])
async def top_balls(ctx):
    guild_id = ctx.guild.id
    top_3_users = sorted(balls_counter[guild_id].items(), key=lambda item: item[1], reverse=True)[:3]
    top_3_mentions = [f'<@{user_id}>' for user_id, count in top_3_users]
    response = '# Top 3 ballers:\n' + '\n'.join([f'{mention}: {count}' for mention, (user_id, count) in zip(top_3_mentions, top_3_users)])
    await ctx.send(response)

@bot.command(name='balls')
async def send_log(ctx):
    log_file_path = get_log_file_path(ctx.guild.id)
    await ctx.author.send(file=discord.File(log_file_path))

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('MTI2MDI0OTE0Njc2NjY1NTUwOQ.GEHbsE.8SxhrzQ4UyVspw06apYlCr2ls-voHsUbGdxNSU')
