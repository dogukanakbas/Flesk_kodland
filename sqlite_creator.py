import sqlite3

def create_db():
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

   
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  score INTEGER,
                  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()

create_db() 
