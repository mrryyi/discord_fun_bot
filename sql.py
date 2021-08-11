import sqlite3

sql_connection = sqlite3.connect('stats.db')

sql_cursor = sql_connection.cursor()

"""
sql_cursor.execute(
          "ALTER TABLE swenglish ADD COLUMN jump_url TEXT")

sql_cursor.execute(
          "DROP TABLE swenglish")

sql_cursor.execute("delete from swenglish where DATETIME(date_time, '+120 minutes') < '2021-08-10 21:12:00'")
sql_cursor.execute("delete from swenglish ")



sql_cursor.execute("delete from swenglish where lower(swenglish_text) like '%yeah%'")


# Remove swenglish based on which user typed it
# Used to remove test cases
sql_cursor.execute(
"DELETE FROM swenglish " 
"WHERE user_id IN ( "
"    SELECT sw.user_id FROM swenglish sw "
"    INNER JOIN users u on u.user_id = sw.user_id "
"    WHERE LOWER(u.combined_name) like '%Ryyi%' and sw.swenglish_text like '%_test_%'"
")"
)

#-------------------------
sql_cursor.execute("SELECT * from short_swedish_words")

list_of_tuples = sql_cursor.fetchall()
words = [word for tuple in list_of_tuples for word in tuple]
#print(list_of_tuples)
for word in words:
    print(word)
#-------------------------

"""


sql_connection.commit()

sql_connection.close()