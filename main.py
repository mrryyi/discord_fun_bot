import discord
import os

from memes_from_reddit import *
from quotes import *
from responsive import *

botclient = discord.Client()

GUILDID = os.getenv('GUILDID')

@botclient.event
async def on_ready():
    print('We have logged in as {0.}')

@botclient.event
async def on_message(message):
    if message.author == botclient.user:
        return

    message_sent = False

    msg = message.content

    response_trigger = get_response_trigger(msg)
    if not message_sent and response_trigger != "":
        response = generate_response_by_trigger(response_trigger)
        await message.channel.send(response)
        message_sent = True
    
    emoji_reactions = get_reactions(msg = msg, available_emojis = botclient.emojis)
    for emoji in emoji_reactions:
        await message.add_reaction(emoji)

    if not message_sent and msg.startswith('.inspire'):
        inspire_quote  = get_inspire_quote()
        await message.channel.send(inspire_quote)
        message_sent = True
    
    if not message_sent and msg.startswith('.meme'):
        await message.channel.send(get_meme_message())
        message_sent = True
    
    if not message_sent and random.randint(1,69) == 42:
        print("ligma balls")
        await message.channel.send("ligma balls")

botclient.run(os.getenv('TOKEN'))