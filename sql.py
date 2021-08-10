import sqlite3

sql_connection = sqlite3.connect('stats.db')

sql_cursor = sql_connection.cursor()

"""
sql_cursor.execute(
          "ALTER TABLE swenglish ADD COLUMN jump_url TEXT")

sql_cursor.execute(
          "DROP TABLE swenglish")

"""
sql_cursor.execute("delete from swenglish where DATETIME(date_time, '+120 minutes') < '2021-08-10 21:12:00'")



sql_connection.commit()

sql_connection.close()