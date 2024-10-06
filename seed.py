import sqlite3
# Run to initialize the database.

# Connecting to a SQLite database
conn = sqlite3.connect('example.db')

# Creating a cursor object to interact with the database
cursor = conn.cursor()

# Example query: Creating a table
cursor.execute('''CREATE TABLE IF NOT EXISTS ImageResizer  (
    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
    originalImage BLOB NOT NULL, 
    size1 BLOB, 
    size2 BLOB, 
    size3 BLOB
);
''')

# Committing the transaction and closing the connection
conn.commit()
conn.close()