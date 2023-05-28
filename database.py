import sqlite3


database_path = 'C:/Users/DELL/Desktop/crud-flask/anju.db'

# Connect to the database or create it if it doesn't exist
connection = sqlite3.connect(database_path)

# Close the connection
connection.close()