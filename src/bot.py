import sys
import ctypes
sys.path.insert(0, 'discord.py-self')
import discord
import numpy as np
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
main_user_id = 'config/bot_id.json'
average_time_interval = []

def set_window_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

with open(settings_file) as file:
    config_data = json.load(file)
    token = config_data['token']
    intervals = config_data['intervals']
    random_channel = config_data['channel_ids']
    prefix = config_data['prefix']

with open(phrases_file) as file:
    phrases_data = json.load(file)
    phrases = phrases_data['phrases']

with open(main_user_id) as file:
    id_data = json.load(file)
    bot_id = id_data['bot_ID']

bot = commands.Bot(command_prefix=prefix, self_bot=True)


@bot.event
async def on_ready():
    bot_id = (bot.user.id)
    id_data['bot_ID'] = bot_id
    with open(main_user_id, 'w') as file:
        json.dump(id_data, file)
    set_window_title("Main token")  # Set the desired window title
    print("Logged in!")
    await send_random_phrase()

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def send_random_phrase():
    def average_interval(min, max, average_time_interval, interval):
        average_time_interval.append(interval)
        return average_time_interval

    x = 1
    
    while True:
        #Making time work
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        #random channel picker
        channel_id = random.choice(random_channel)
        channel_name = bot.get_channel(int(channel_id))

        # Generate a random interval between min and max (in seconds)
        interval = random.randint(intervals['min'], intervals['max'])

        # Choose a random phrase from the list
        phrase = random.choice(phrases)

        #message count sender
        if x<=1:
            print('(', time, ')','|', {bot.user.name}, ': Has send ', x, 'Messages', '|', 'Message sent in', ':', channel_name)
            x=x+1
        else:
            print('(', time, ')','|', {bot.user.name}, ': Has send ', x, 'Messages', '|', 'Message sent in', ':', channel_name, '|', 'The bot will take', interval, 'seconds to send a message')
            x=x+1

        # Send the random phrase to the specified channel
        channel = bot.get_channel(int(channel_id))
        await channel.send(phrase)


        # Wait for the interval before sending the next random phrase
        await asyncio.sleep(interval)

bot.run(token)
