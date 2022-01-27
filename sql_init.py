from sql_lib import *

def create_swedish_words_table(sql_cursor, sql_connection):
    sql_cursor.execute("CREATE TABLE IF NOT EXISTS short_swedish_words"
          "("
          "word TEXT(500) NOT NULL UNIQUE"
          ")")
    sql_connection.commit()

def create_users_table(sql_cursor, sql_connection):
    sql_cursor.execute(
          "CREATE TABLE IF NOT EXISTS users"
          "("
          "user_id TEXT PRIMARY KEY NOT NULL UNIQUE,"
          "combined_name TEXT NOT NULL"
          ")")
    sql_connection.commit()

def create_swenglish_words_table(sql_cursor, sql_connection):
    sql_cursor.execute(
        "CREATE TABLE IF NOT EXISTS swenglish"
        "("
        "swenglish_text TEXT(500) NOT NULL,"
        "user_id TEXT NOT NULL,"
        "date_time datetime,"
        "jump_url TEXT,"
        "FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE"
        ")")
    sql_connection.commit()

def create_configuration_table(sql_cursor, sql_connection):
    sql_cursor.execute(
          "CREATE TABLE IF NOT EXISTS configurations"
          "("
          "configuration TEXT PRIMARY KEY NOT NULL UNIQUE,"
          "toggled INTEGER DEFAULT 0 NOT NULL, "
          "value_configuration INTEGER DEFAULT 0, "
          "range_min INTEGER DEFAULT 0, "
          "range_max INTEGER DEFAULT 0 "
          ")")
    sql_connection.commit()

def initiate_default_configurations_table(sql_cursor, sql_connection):
    file = open("initconfig\\defaultconfig.txt", 'r')
    configurations = file.readlines()

    for configuration in configurations:
        configuration = configuration.replace('\n','')
        insert_new_configuration(sql_cursor, sql_connection, configuration)