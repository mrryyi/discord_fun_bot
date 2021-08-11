import sqlite3

sql_connection = sqlite3.connect('stats.db')
sql_cursor = sql_connection.cursor()

def load_short_swedish():
    with open('words/short_swedish_words.txt') as words:
        lines = set(words.read().split('\n'))
    
    data = []
    for line in lines:
        word = line.split(' ')[0]
        if len(word) == 2:
            data.append(word)
    return data

def add_short_swedish_word(sql_cursor, short_swedish_word):
    if len(word) == 2:
        try:
            sql_cursor.execute("INSERT INTO short_swedish_words(word) VALUES(?)", (short_swedish_word,))
        except sqlite3.IntegrityError:
            print("Word already exists")
            return

if __name__ == '__main__':
    data = load_short_swedish()
    
    sql_connection = sqlite3.connect('stats.db')
    sql_cursor = sql_connection.cursor()
    
    sql_cursor.execute("CREATE TABLE IF NOT EXISTS short_swedish_words"
          "("
          "word TEXT(500) NOT NULL UNIQUE"
          ")")
    

    for word in data:
        # Insert into short_swedish_words
        add_short_swedish_word(sql_cursor, word)

    sql_connection.commit()
    sql_connection.close()
