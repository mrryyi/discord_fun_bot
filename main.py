import discord
import os
import sys
import sqlite3

from memes_from_reddit import *
from swenglish_detection import *
from quotes import *
from responsive import *

print(sys.version)

botclient = discord.Client()

GUILDID = os.getenv('GUILDID')
BOTOWNER = os.getenv('BOTOWNER')

sql_connection = sqlite3.connect('stats.db')

sql_cursor = sql_connection.cursor()

sql_cursor.execute(
          "CREATE TABLE IF NOT EXISTS users"
          "("
          "user_id TEXT PRIMARY KEY NOT NULL UNIQUE,"
          "combined_name TEXT NOT NULL"
          ")")

sql_cursor.execute(
          "CREATE TABLE IF NOT EXISTS swenglish"
          "("
          "swenglish_text TEXT(500) NOT NULL,"
          "user_id TEXT NOT NULL,"
          "date_time datetime,"
          "jump_url TEXT,"
          "FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE"
          ")")
        
sql_cursor.execute("CREATE TABLE IF NOT EXISTS short_swedish_words"
          "("
          "word TEXT(500) NOT NULL UNIQUE"
          ")")

sql_connection.commit()

def register_user(user):
    
    try:
        print_user(user)
        sql_cursor.execute("INSERT INTO users(user_id, combined_name) VALUES(?,?)",
            (user.id, combine_name_discriminator(user)))
    except sqlite3.IntegrityError:
        # User is already registered
        return
    sql_connection.commit()

def update_swenglish_table(context):
    sql_cursor.execute("INSERT INTO swenglish(swenglish_text, user_id, date_time, jump_url) VALUES(?,?,CURRENT_TIMESTAMP,?)",
        (context.content, context.author.id, context.jump_url))
    sql_connection.commit()
    print("INSERTED NEW SWENGLISH TEXT")

def get_swenglish_messages():
    sql_cursor.execute("SELECT "
                       "u.combined_name as username,"
                       "swenglish_text as swenglish, "
                       "strftime('%Y-%m-%d %H:%M:%S', DATETIME(sw.date_time, '+120 minutes')) as datetime, "
                       "jump_url "
                       "FROM swenglish sw "
                       "inner join users u on sw.user_id = u.user_id")
    data = sql_cursor.fetchall()
    return data

def get_swenglish_counts():
    sql_cursor.execute("SELECT "
                       "u.combined_name as username,"
                       "COUNT(sw.ROWID) as swenglish_count "
                       "FROM swenglish sw "
                       "inner join users u on sw.user_id = u.user_id "
                       "group by username "
                       "order by count(sw.ROWID) desc")
    data = sql_cursor.fetchall()
    return data


def show_swenglish_table():
    data = get_swenglish_messages()
    print(data)


def combine_name_discriminator(user):
    return user.name + "#" + user.discriminator

def print_user(user):
    print(user.id)
    print(combine_name_discriminator(user))

def handle_swenglish(context):
    sql_cursor.execute("SELECT * from short_swedish_words")
    list_of_tuples = sql_cursor.fetchall()
    short_swedish_words = [word for tuple in list_of_tuples for word in tuple]

    swenglish_data = get_swenglish_data(short_swedish_words, context.content.lower())
    swenglish_verdict = swenglish_data["swenglish_verdict"]
    if swenglish_verdict == "swenglish":
        update_swenglish_table(context)

async def handle_response_trigger(context):
    response_trigger = get_response_trigger(context.content.lower())
    if response_trigger != "":
        response = generate_response_by_trigger(response_trigger)
        await context.channel.send(response)
        return True

async def handle_atting(context):
    if str(botclient.user.id) in context.content:
        if "Gustaf" in context.author.name:
            await context.channel.send("don't @ me autism looking ass")
        else:
            await context.channel.send("don't @ me")
        return True
    

async def reaction(context):
    emoji_reactions = get_reactions(msg = context.content.lower(), available_emojis = botclient.emojis)
    for emoji in emoji_reactions:
        await context.add_reaction(emoji)

@botclient.event
async def on_ready():
    print("We have logged in as " + botclient.user.name + "#" + botclient.user.discriminator)

@botclient.event
async def on_message(context):
    if context.author == botclient.user:
        return
    
    message_sent = False

    register_user(context.author)

    combined_author_name = combine_name_discriminator(context.author)    

    msg = context.content
    lower_msg = msg.lower()
    
    print("Message: ["+ lower_msg + "]")

    if not message_sent:
        message_sent = await handle_response_trigger(context)
    
    if not message_sent:
        message_sent = await handle_atting(context)
    
    handle_swenglish(context)
    await reaction(context)

    if not message_sent and lower_msg.startswith('.inspire'):
        await context.channel.send(get_inspire_quote())
        message_sent = True

    if not message_sent and lower_msg.startswith('.meme'):
        await context.channel.send(get_meme_message())
        message_sent = True
    
    if lower_msg.startswith('.debug_sql_swenglish'):
        show_swenglish_table()
    
    if lower_msg.startswith('.swenglish_so_far'):# and combined_author_name == BOTOWNER:
        swenglish_table = get_swenglish_messages()
        message = ""
        for row in swenglish_table:
            username = row[0]
            swenglish = row[1]
            datetime = row[2]
            url = row[3]
            if url and 'link' in lower_msg:
                message += "[" + datetime + "] " + username + ": " + swenglish + " " + url + "\n"
            else:
                message += "[" + datetime + "] " + username + ": " + swenglish + "\n"

        await context.channel.send(message)
        message_sent = True
    
    if lower_msg.startswith('.swenglish_count'):# and combined_author_name == BOTOWNER:
        swenglish_table = get_swenglish_counts()
        message = ""
        for row in swenglish_table:
            username = row[0]
            swenglish_count = row[1]
            message += username + ": " + str(swenglish_count) + "\n"

        await context.channel.send(message)
        message_sent = True

    if combined_author_name == BOTOWNER:
        if not message_sent:
            unique_response = get_unique_response(msg = lower_msg)
            if unique_response:
                await context.delete()
                await context.channel.send(unique_response)
                message_sent = True

    
    if not message_sent and random.randint(1,69) == 42:
        print("ligma balls")
        await context.channel.send("ligma balls")

if __name__ == "__main__":
    botclient.run(os.getenv('TOKEN'))
    sql_connection.close()