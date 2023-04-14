from flask import Flask, request, jsonify
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('msgapi.db')
cursor = conn.cursor()

# Execute an SQL query
cursor.execute('SELECT * FROM Messages')
rows = cursor.fetchall()

# Process the fetched rows
for row in rows:
    # Access columns by index (0-based) or by name
    id = row[0]
    sender = row[1]
    recipient = row[2]
    message = row[3]
    datetime = row[4]
    print(f'id: {id}, sender: {sender}, recipient: {recipient}, message: {message}, datetime: {datetime}')

# Close the database connection
conn.close()
