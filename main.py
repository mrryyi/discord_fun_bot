import discord
import os
import sys
import sqlite3
import datetime

from config import *
from sql_lib import *
from sql_init import *
from memes_from_reddit import *
from swenglish_detection import *
from quotes import *
from responsive import *
from funcdump import *

print(sys.version)

botclient = discord.Client()

GUILDID = os.getenv('GUILDID')
BOTOWNER = os.getenv('BOTOWNER')

sql_connection = sqlite3.connect('stats.db')
sql_cursor = sql_connection.cursor()

create_configuration_table(sql_cursor, sql_connection)
create_users_table(sql_cursor, sql_connection)
create_swenglish_words_table(sql_cursor, sql_connection)
initiate_default_configurations_table(sql_cursor, sql_connection)

def register_user(user):
    try:
        sql_cursor.execute("INSERT INTO users(user_id, combined_name) VALUES(?,?)",
            (user.id, combine_name_discriminator(user)))
    except sqlite3.IntegrityError:
        # User is already registered
        return
    sql_connection.commit()

def update_swenglish_table(context):

    #created_at = datetime.date.fromisoformat(context.created_at)
    date = context.created_at.strftime('%Y-%m-%d %H:%M:%S')

    sql_cursor.execute("INSERT INTO swenglish(swenglish_text, user_id, date_time, jump_url) VALUES(?,?,?,?)",
        (context.content, context.author.id, date, context.jump_url))
    sql_connection.commit()

async def get_message_by_url(url):
    split_link = url.split('/')
    server_id  = int(split_link[4])
    channel_id = int(split_link[5])
    message_id = int(split_link[6])
    server = botclient.get_guild(server_id)
    channel = server.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    return message

async def add_swenglish_by_message_url(url):
        if message_url_is_valid(url):
            swenglish_message = await get_message_by_url(url)
            update_swenglish_table(swenglish_message)
        else:
            return

def message_url_is_valid(url):
    return "https" in url and "discord" in url and "channel" in url
        

async def add_swenglish_by_url_command(context):
    if " " in context.content:
        url = context.content.split(' ')[1]
        if message_url_is_valid(url):
            await add_swenglish_by_message_url(url)
        else:
            return

async def load_swenglish_urls():
    with open('words/swenglish_urls.txt') as words:
        lines = set(words.read().split('\n'))
    
    for line in lines:
        await add_swenglish_by_message_url(line)


def get_swenglish_messages():
    sql_cursor.execute("SELECT "
                       "u.combined_name as username,"
                       "swenglish_text as swenglish, "
                       "strftime('%Y-%m-%d %H:%M:%S', DATETIME(sw.date_time, '+120 minutes')) as datetime, "
                       "jump_url "
                       "FROM swenglish sw "
                       "inner join users u on sw.user_id = u.user_id "
                       "order by datetime desc")
    data = sql_cursor.fetchall()
    return data

def get_swenglish_message_latest():
    sql_cursor.execute("SELECT "
                       "u.combined_name as username,"
                       "swenglish_text as swenglish, "
                       "strftime('%Y-%m-%d %H:%M:%S', DATETIME(sw.date_time, '+120 minutes')) as datetime, "
                       "jump_url "
                       "FROM swenglish sw "
                       "inner join users u on sw.user_id = u.user_id "
                       "order by datetime desc "
                       "LIMIT 1"
                       )
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

def get_random_swenglish():

    sql_cursor.execute("SELECT COUNT(*) FROM swenglish")
    data = sql_cursor.fetchall()
    count_of_rows = data[0][0]
    random_offset = random.randint(0, count_of_rows)

    sql_cursor.execute("SELECT "
                       "u.combined_name as username,"
                       "swenglish_text as swenglish, "
                       "strftime('%Y-%m-%d %H:%M:%S', DATETIME(sw.date_time, '+120 minutes')) as datetime, "
                       "jump_url "
                       "FROM swenglish sw "
                       "inner join users u on sw.user_id = u.user_id "
                       "order by datetime desc "
                       "LIMIT 1 OFFSET " + str(random_offset))

    data = sql_cursor.fetchall()

    row = data[0]
    username = row[0]
    swenglish = row[1]
    if '@' in swenglish:
        swenglish = swenglish.replace('@','')
    datetime = row[2]
    url = row[3]

    if url:
        message_line = "[" + datetime + "] " + username + ": " + swenglish + " " + url + "\n"
    else:
        message_line = "[" + datetime + "] " + username + ": " + swenglish + "\n"
    
    return message_line
    

def handle_swenglish(context):
    sql_cursor.execute("SELECT * from short_swedish_words")
    list_of_tuples = sql_cursor.fetchall()
    short_swedish_words = [word for tuple in list_of_tuples for word in tuple]

    swenglish_data = get_swenglish_data(short_swedish_words, context.content.lower())
    swenglish_verdict = swenglish_data["swenglish_verdict"]
    if swenglish_verdict == "swenglish":
        update_swenglish_table(context)
        print(*swenglish_data["english_words"])
        print("INSERTED NEW SWENGLISH TEXT")

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
    combined_author_name = combine_name_discriminator(context.author)    
    author_sent_message = combined_author_name == BOTOWNER
    msg = context.content
    lower_msg = msg.lower()
    channel = context.channel
    guild = context.guild

    register_user(context.author)
    print("[" + str(guild) + "\\" + str(channel) + "] [" + combined_author_name + "]: "+ lower_msg)

    config = load_configurations(sql_cursor)

    if not config:
        print("configurations failed to load")

    if not message_sent:
        message_sent = await handle_atting(context)

    message_is_command = lower_msg.startswith('.')

    if not message_is_command:
        if config["reactions"].toggled == 1:
            await reaction(context)
        
        if config["responses"].toggled == 1:
            if not message_sent:
                if random.randint(1,10) == 2:
                    message_sent = await handle_response_trigger(context)
    
    splat_msg = msg.split(" ")

    if message_is_command:
        if not message_sent and lower_msg.startswith('.toggle'):
            config_answer = "Something went wrong"
            if not len(splat_msg) > 1:
                config_answer = "Invalid command. Please supply configuration to toggle."
            else:
                config_to_toggle = splat_msg[1].lower()
                ret = toggle_configuration(sql_cursor, sql_connection, config_to_toggle)
                if ret == "toggledoff":
                    config_answer = config_to_toggle + " toggled off."
                elif ret == "toggledon":
                    config_answer = config_to_toggle + " toggled on."
                elif ret ==  "undefined":
                    config_answer = config_to_toggle + " had weird toggle value."
                elif ret == "notfound":
                    config_answer = config_to_toggle + " not found as configuration."
                
            await context.channel.send(config_answer)

        if not message_sent and lower_msg.startswith('.showconfig'):
            verbose = False
            
            if len(splat_msg) > 1:
                if splat_msg[1].lower() == 'verbose':
                    verbose = True
            
            message_lines = []
            message_line = ""
            length_so_far = 0
            for config_name in config:
                toggled = config[config_name].toggled
                value_configuration = config[config_name].value_configuration
                range_min = config[config_name].range_min
                range_max = config[config_name].range_max
                
                if toggled == 1:
                    toggled_str = "on"
                else:
                    toggled_str = "off"
                
                if verbose:
                    message_line = "["+config_name+"]: toggled "+toggled_str+", value_configuration="+str(value_configuration)+", range_min="+str(range_min)+", range_max="+str(range_max)+"\n"
                else:
                    message_line = "["+config_name+"]: toggled "+toggled_str+"\n"

                if length_so_far + len(message_line) <= 2000:
                    length_so_far += len(message_line)
                    message_lines.append(message_line)
                else:
                    break

            message = ""
            message_lines.reverse()
            for line in message_lines:
                message += line

            await context.channel.send(message)
            message_sent = True


        if not message_sent and lower_msg.startswith('.spoiler'):
            spoiler_message = "[" + combined_author_name + "]: "+ "||" + msg + "||"
            spoiler_message = spoiler_message.replace(".spoiler","",1)
            await context.delete()
            await context.channel.send(spoiler_message)
            message_sent = True

        if not message_sent and lower_msg.startswith('.inspire'):
            await context.channel.send(get_inspire_quote())
            message_sent = True
        
        if not message_sent and lower_msg.startswith('.uninspire'):
            await context.channel.send(get_uninspire_quote())
            message_sent = True

        if not message_sent and lower_msg.startswith('.meme'):
            while not message_sent:
                try:
                    await context.channel.send(get_meme_message())
                    message_sent = True
                except ValueError:
                    print("ValueError :( trying again")

        if lower_msg.startswith('.swengdbg'):
            show_swenglish_table()
            print_swenglish_messages(sql_cursor)
            message_sent = True

        if not message_sent and lower_msg.startswith('.swengcount'):# and combined_author_name == BOTOWNER:
            swenglish_table = get_swenglish_counts()
            message = ""
            for row in swenglish_table:
                username = row[0]
                swenglish_count = row[1]
                message += username + ": " + str(swenglish_count) + "\n"

            await context.channel.send(message)
            message_sent = True
        
        if not message_sent and lower_msg.startswith('.swenglatest'):
            swenglish_table = get_swenglish_message_latest()
            message_lines = []
            message_line = ""
            length_so_far = 0
            for row in swenglish_table:
                username = row[0]
                swenglish = row[1]
                if '@' in swenglish:
                    swenglish = swenglish.replace('@','')
                datetime = row[2]
                url = row[3]
                if url and 'link' in lower_msg:
                    message_line = "[" + datetime + "] " + username + ": " + swenglish + " " + url + "\n"
                else:
                    message_line = "[" + datetime + "] " + username + ": " + swenglish + "\n"

                if length_so_far + len(message_line) <= 2000:
                    length_so_far += len(message_line)
                    message_lines.append(message_line)
                else:
                    break
                break
            
            message = ""
            message_lines.reverse()
            for line in message_lines:
                message += line
            if message:
                await context.channel.send(message)
                message_sent = True

        if not message_sent and lower_msg.startswith('.sweng'):
            swenglish_table = get_swenglish_messages()
            message_lines = []
            message_line = ""
            length_so_far = 0
            for row in swenglish_table:
                username = row[0]
                swenglish = row[1]
                if '@' in swenglish:
                    swenglish = swenglish.replace('@','')
                datetime = row[2]
                url = row[3]
                if url and 'link' in lower_msg:
                    message_line = "[" + datetime + "] " + username + ": " + swenglish + " " + url + "\n"
                else:
                    message_line = "[" + datetime + "] " + username + ": " + swenglish + "\n"

                if length_so_far + len(message_line) <= 2000:
                    length_so_far += len(message_line)
                    message_lines.append(message_line)
                else:
                    break
            
            message = ""
            message_lines.reverse()
            for line in message_lines:
                message += line

            await context.channel.send(message)
            message_sent = True
    
        if lower_msg.startswith('.addsweng'):
            await add_swenglish_by_url_command(context)
        
        if lower_msg.startswith('.randomsweng'):
            swenglish_random = get_random_swenglish()
            await context.channel.send(swenglish_random)

        if lower_msg.startswith('.load') and author_sent_message:
            await load_swenglish_urls()

    if author_sent_message:
        if not message_sent:
            unique_response = get_unique_response(msg = lower_msg)
            if unique_response:
                await context.delete()
                await context.channel.send(unique_response)
                message_sent = True
    
    if not message_sent and random.randint(1,420) == 69:
        print("ligma balls")
        await context.channel.send("ligma balls")

if __name__ == "__main__":
    botclient.run(os.getenv('TOKEN'))
    sql_connection.close()