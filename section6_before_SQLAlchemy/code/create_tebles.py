import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_talbe = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"  # we are going to create a table with an auto-incrementing id
cursor.execute(create_talbe)

create_talbe = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_talbe)


connection.commit()
connection.close()

