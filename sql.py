import sqlite3

sql_connection = sqlite3.connect('stats.db')

sql_cursor = sql_connection.cursor()

sql_cursor.execute(
          "ALTER TABLE swenglish ADD COLUMN jump_url TEXT")

sql_connection.commit()

sql_connection.close()