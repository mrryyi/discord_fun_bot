import sqlite3
from sql_lib import *

sql_connection = sqlite3.connect('stats.db')
sql_cursor = sql_connection.cursor()

# Call functions here
#import_swenglish_list(sql_cursor)
#print_swenglish_messages(sql_cursor)
#delete_swenglish_by_date(sql_cursor, "2021-07-23")
#delete_swenglish_by_date(sql_cursor, "2021-07-28")
#delete_swenglish_with_word(sql_cursor, "oliver")
#delete_swenglish_with_word(sql_cursor, "yhea")


"""
sql_cursor.execute(
          "ALTER TABLE swenglish ADD COLUMN jump_url TEXT")

sql_cursor.execute(
          "DROP TABLE swenglish")

sql_cursor.execute("delete from swenglish where DATETIME(date_time, '+120 minutes') < '2021-08-10 21:12:00'")

sql_cursor.execute(
          "DELETE from swenglish where swenglish_text LIKE '%nog all of us%' ")
          
sql_cursor.execute(
          "ALTER TABLE swenglish ADD COLUMN count_of_selections INT")
"""
sql_connection.commit()

sql_connection.close()

