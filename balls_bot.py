import discord
from discord.ext import commands
from collections import defaultdict
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
balls_counter = defaultdict(lambda: defaultdict(int))
log_directory = 'balls_bot'

# Function to get log file path for a guild
def get_log_file_path(guild_id):
    return os.path.join(log_directory, f'balls_log_{guild_id}.txt')

# Function to read logs and update memory on bot startup
def read_logs_and_update_memory():
    for filename in os.listdir(log_directory):
        if filename.endswith('.txt'):
            guild_id = int(filename.split('_')[2].split('.')[0])  # Extract guild ID from filename
            log_file_path = os.path.join(log_directory, filename)
            with open(log_file_path, 'r') as f:
                for line in f:
                    user, count = line.strip().split(', ')
                    balls_counter[guild_id][user] = int(count)

# Event: When bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} ready to ball')
    read_logs_and_update_memory()

# Event: When a message is received
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    if 'balls' in message.content.lower() and not message.content.startswith('!'):
        await message.channel.send('balls')
        
        guild_id = message.guild.id
        user_id = str(message.author.id)
        
        # Update memory
        balls_counter[guild_id][user_id] += 1
        
        # Update log file
        log_file_path = get_log_file_path(guild_id)
        with open(log_file_path, 'a') as f:
            f.write(f'{user_id}, {balls_counter[guild_id][user_id]}\n')
    
    await bot.process_commands(message)


@bot.command(name='topballs', aliases=['top', 'ballers', 'topballers','baller'])
async def top_balls(ctx, n: int = 3):
    guild_id = ctx.guild.id
    log_file_path = get_log_file_path(guild_id)
    
    # Read log file and parse counts
    user_counts = {}
    with open(log_file_path, 'r') as f:
        for line in f:
            user, count = line.strip().split(', ')
            user_counts[user] = int(count)
    
    # Sort users by count and get top n
    top_users = sorted(user_counts.items(), key=lambda item: item[1], reverse=True)[:n]
    
    # Prepare response message
    response = f'# Top {n} ballers:\n'
    for idx, (user, count) in enumerate(top_users, start=1):
        member = ctx.guild.get_member(int(user))
        username = member.display_name if member else f'User ID: {user}'
        response += f'{idx}. {username}: {count}\n'
    
    # Send the message
    await ctx.send(response)

bot.run('balls_bot_token')