import sys
import ctypes
sys.path.insert(0, 'discord.py-self')
import discord
from discord.ext import commands
from datetime import datetime
import aiohttp
import asyncio
import json
import re
import tracemalloc
import os
import requests
import random
tracemalloc.start()

settings_file = 'config/config.json'
phrases_file = 'config/phrases.json'
bot_file = 'config/Bot_id.json'

def set_window_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

with open(settings_file) as file:
    config_data = json.load(file)
    token = config_data['token_1']
    intervals = config_data['intervals']
    random_channel = config_data['channel_ids']
    prefix = config_data['prefix']

with open(phrases_file) as file:
    phrases_data = json.load(file)
    phrases = phrases_data['phrases']

with open(bot_file) as file:
    bot_data = json.load(file)
    bot_id = bot_data['bot_ID']

bot = commands.Bot(command_prefix=prefix, self_bot=True)

@bot.event
async def on_ready():
    print("Logged in!")
    set_window_title("Extra token")  # Set the desired window title


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")



phrase = random.choice(phrases)

@bot.event
async def on_message(message):
    x=1
    if message.author.id == bot_id:
        interval = random.randint(3, 7)
        await asyncio.sleep(interval)
        
        await message.channel.send(phrase)
        #Making time work
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print('(', time, ')','|', {bot.user.name},'The bot will take', interval, 'seconds to send a message')

        x=x+1
        
        
        

bot.run(token)
