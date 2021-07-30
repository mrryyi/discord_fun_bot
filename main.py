import discord
import os
import sys

from memes_from_reddit import *
from quotes import *
from responsive import *

print(sys.version)

botclient = discord.Client()

GUILDID = os.getenv('GUILDID')
BOTOWNER = os.getenv('BOTOWNER')

@botclient.event
async def on_ready():
    print("We have logged in as " + botclient.user.name + "#" + botclient.user.discriminator)

@botclient.event
async def on_message(message):
    if message.author == botclient.user:
        return

    author = message.author.name + "#" + message.author.discriminator
    
    message_sent = False

    msg = message.content
    lower_msg = msg.lower()

    response_trigger = get_response_trigger(msg = lower_msg)
    if not message_sent and response_trigger != "":
        response = generate_response_by_trigger(response_trigger)
        await message.channel.send(response)
        message_sent = True

    emoji_reactions = get_reactions(msg = lower_msg, available_emojis = botclient.emojis)
    for emoji in emoji_reactions:
        await message.add_reaction(emoji)

    if not message_sent and lower_msg.startswith('.inspire'):
        await message.channel.send(get_inspire_quote())
        message_sent = True

    if not message_sent and lower_msg.startswith('.meme'):
        await message.channel.send(get_meme_message())
        message_sent = True

    if author == BOTOWNER:
        if not message_sent:
            unique_response = get_unique_response(msg = lower_msg)
            if unique_response:
                await message.delete()
                await message.channel.send(unique_response)
                message_sent = True

    
    if not message_sent and random.randint(1,69) == 42:
        print("ligma balls")
        await message.channel.send("ligma balls")

botclient.run(os.getenv('TOKEN'))