import sqlite3
import discord
from datatypes import Configuration

def toggle_configuration(sql_cursor, sql_connection, configuration):
    sql_cursor.execute("SELECT * FROM configurations c where c.configuration = '" + configuration + "'")

    row = sql_cursor.fetchone()
    if row is not None:
        toggled = row[1] # toggled column
        if toggled == 1:
            sql_cursor.execute("UPDATE configurations SET toggled = 0 WHERE configuration = '" + configuration + "'")
            sql_connection.commit()
            return "toggledoff"
        elif toggled == 0:
            sql_cursor.execute("UPDATE configurations SET toggled = 1 WHERE configuration = '" + configuration + "'")
            sql_connection.commit()
            return "toggledon"
        return "undefined"

    # Could not toggle
    return "notfound"

def insert_new_configuration(sql_cursor, sql_connection, configuration_name):
    sql_cursor.execute("SELECT * from configurations c where c.configuration = '" + configuration_name + "'")
    row = sql_cursor.fetchone()
    if not row:
        print("inserting " + configuration_name)
        toggled = "0"
        value_configuration = "0"
        range_min = "0"
        range_max = "0"
        sql_cursor.execute("INSERT OR IGNORE INTO configurations(configuration, toggled, value_configuration, range_min, range_max) VALUES(?,?,?,?,?)",
                                                                (configuration_name, toggled, value_configuration, range_min, range_max))
        sql_connection.commit()
    else:
        print("NOT inserting " + configuration_name)

def load_configurations(sql_cursor):
    sql_cursor.execute("SELECT * from configurations")
    configuration_table = sql_cursor.fetchall()
    config_dict = {}
    for row in configuration_table:
        config_dict[row[0]] = Configuration(row[1], row[2], row[3], row[4])
    return config_dict

def print_swenglish_messages(sql_cursor):
    sql_cursor.execute("SELECT "
                       "u.combined_name as username,"
                       "swenglish_text as swenglish, "
                       "strftime('%Y-%m-%d %H:%M:%S', DATETIME(sw.date_time, '+120 minutes')) as datetime, "
                       "jump_url "
                       "FROM swenglish sw "
                       "inner join users u on sw.user_id = u.user_id "
                       "order by datetime desc")
    swenglish_table = sql_cursor.fetchall()

    message_lines = []
    message_line = ""
    for row in swenglish_table:
        username = row[0]
        swenglish = row[1]
        if '@' in swenglish:
            swenglish = swenglish.replace('@','')
        datetime = row[2]
        url = row[3]
        if url:
            message_line = "[" + datetime + "] " + username + ": " + swenglish + " " + url
        else:
            message_line = "[" + datetime + "] " + username + ": " + swenglish

        message_lines.append(message_line)
    
    message_lines.reverse()
    messages = ""
    for line in message_lines:
        messages += line + "\n"

    print(messages)    

def delete_swenglish_by_date(sql_cursor, date_time):
    # Remove swenglish based on which user typed it
    # Used to remove test cases
    sql_cursor.execute(
    "DELETE FROM swenglish where strftime('%Y-%m-%d', date_time) = '" + date_time + "'" 
    )

def delete_swenglish_by_user_and_word(sql_cursor, user, word):
    # Remove swenglish based on which user typed it
    # Used to remove test cases
    sql_cursor.execute(
    "DELETE FROM swenglish " 
    "WHERE user_id IN ( "
    "    SELECT sw.user_id FROM swenglish sw "
    "    INNER JOIN users u on u.user_id = sw.user_id "
    "    WHERE (LOWER(u.combined_name) like '%" + user.lower() + "%')"
    ")   and (LOWER(swenglish_text) like '%" + word.lower() + "%')"
    )



def delete_swenglish_with_word(sql_cursor, word):
    sql_cursor.execute("delete from swenglish where lower(swenglish_text) like '%" + word + "%'")

def print_short_swedish_words(sql_cursor):
    sql_cursor.execute("SELECT * from short_swedish_words")

    list_of_tuples = sql_cursor.fetchall()
    words = [word for tuple in list_of_tuples for word in tuple]
    #print(list_of_tuples)
    for word in words:
        print(word)

def import_swenglish_list(sql_cursor):
    swenglish_list = [
    ("Men jesus Stevo's röst är beyond fucked","2021-07-23"),
    ("Decades av negligence","2021-07-28")
    ]

    for swenglish in swenglish_list:
        sql_cursor.execute("INSERT INTO swenglish(swenglish_text, user_id, date_time) VALUES(?,?,?)",
                (swenglish[0], 144503258646446080, swenglish[1]))
