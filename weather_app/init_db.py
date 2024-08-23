import sqlite3

def init_db():
    # Connect to SQLite database (it will create the database file if it doesn't exist)
    conn = sqlite3.connect('weather_data.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table to store weather records
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY,
        city TEXT NOT NULL,
        temperature REAL NOT NULL,
        pressure INTEGER NOT NULL,
        humidity INTEGER NOT NULL,
        description TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
