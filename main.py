import discord
import random
import asyncio
import json

client = discord.Client()

settings_file = 'config.json'
phrases_file = 'phrases.json'

#json file loaders
with open(settings_file) as file:
    config_data = json.load(file)
    token = config_data['token']
    intervals = config_data['intervals']
    random_channel = config_data['channel_ids']

with open(phrases_file) as file:
    phrases_data = json.load(file)
    phrases = phrases_data['phrases']

#bot starter key
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

    # Start the random phrase sending loop
    await send_random_phrase()


#function for random message
async def send_random_phrase():
    x = 1
    while True:
        #message counter

        #random channel picker
        channel_id = random.choice(random_channel)

        # Choose a random phrase from the list
        phrase = random.choice(phrases)

        #message count sender
        print("Number of messages send :", x)
        x=x+1

        # Send the random phrase to the specified channel
        channel = client.get_channel(int(channel_id))
        await channel.send(phrase)

        # Generate a random interval between min and max (in seconds)
        interval = random.randint(intervals['min'], intervals['max'])

        # Wait for the interval before sending the next random phrase
        await asyncio.sleep(interval)


#engine
client.run(token)
