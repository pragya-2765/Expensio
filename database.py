import sqlite3
DB_NAME = "expenses.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)     #conn object is used to interact with db
    conn.row_factory = sqlite3.Row      #returns each row as dictionary-like object
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()         #tool to execute sql command
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()       #save changes
    conn.close()