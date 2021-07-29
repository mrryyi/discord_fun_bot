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

    msg = message.content

    response_trigger = get_response_trigger(msg)
    if response_trigger != "":
        response = generate_response_by_trigger(response_trigger)
        await message.channel.send(response)
    
    emoji_reaction_names = get_reactions(msg)
    for emoji in botclient.emojis:
        for emoji_reaction_name in emoji_reaction_names:
            if emoji_reaction_name == emoji.name:
                await message.add_reaction(emoji)

    if msg.startswith('.hello'):
        await message.channel.send('Hello!')
    
    if msg.startswith('.inspire'):
        inspire_quote  = get_inspire_quote()
        await message.channel.send(inspire_quote)
    
    if msg.startswith('.meme'):
        await message.channel.send(get_meme_message())

botclient.run(os.getenv('TOKEN'))