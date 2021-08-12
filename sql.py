import sqlite3
from sql_lib import *

sql_connection = sqlite3.connect('stats.db')
sql_cursor = sql_connection.cursor()

# Call functions here
#import_swenglish_list(sql_cursor)
print_swenglish_messages(sql_cursor)
#delete_swenglish_by_date(sql_cursor, "2021-07-23")
#delete_swenglish_by_date(sql_cursor, "2021-07-28")
#delete_swenglish_with_word(sql_cursor, "oliver")
#delete_swenglish_with_word(sql_cursor, "yhea")

sql_connection.commit()

sql_connection.close()

