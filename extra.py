import discord
import random
import asyncio
import json
from datetime import datetime

client = discord.Client()

#importing json files
settings_file = 'config.json'
phrases_file = 'phrases.json'

#Making time work

now = datetime.now()
time_ = now.strftime("%H:%M:%S")


#json file loaders
with open(settings_file) as file:
    config_data = json.load(file)
    token_1 = config_data['token_1']
    intervals = config_data['intervals']
    random_channel = config_data['channel_ids']

with open(phrases_file) as file:
    phrases_data = json.load(file)
    phrases = phrases_data['phrases']

#bot starter key
@client.event
async def on_ready():
    print('(', time_, ')','|', 'Logged in as', {client.user.name})

    # Start the random phrase sending loop
    await send_random_phrase()


#function for random message
async def send_random_phrase():
    x = 1

    while True:
        #Making time work
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        #random channel picker
        channel_id = random.choice(random_channel)
        channel_name = client.get_channel(int(channel_id))

        # Generate a random interval between min and max (in seconds)
        interval = random.randint(intervals['min'], intervals['max'])

        # Choose a random phrase from the list
        phrase = random.choice(phrases)

        #message count sender
        if x<=1:
            print('(', time, ')','|', {client.user.name}, ': Has send ', x, 'Message', '|', 'Message sent in', ':', channel_name,)
            x=x+1
        else:
            print('(', time, ')','|', {client.user.name}, ': Has send ', x, 'Messages', '|', 'Message sent in', ':', channel_name, '|', 'Has taken', interval, 'seconds to send a message')
            x=x+1

        # Send the random phrase to the specified channel
        channel = client.get_channel(int(channel_id))
        await channel.send(phrase)


        # Wait for the interval before sending the next random phrase
        await asyncio.sleep(interval)


#engine
client.run(token_1)