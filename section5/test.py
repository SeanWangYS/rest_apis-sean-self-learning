import sqlite3
from sqlite3.dbapi2 import connect

connection = sqlite3.connect('data.db')

# cursor allow you select things and start things.
# the cursor is response for actually executing the queries
cursor = connection.cursor() 

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

# insert single user
user = (1, 'jose', 'asdf')
insert_query = 'INSERT INTO users VALUES (?, ?, ?)'
cursor.execute(insert_query, user)


# inser multiple users
users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'zxcv')
]
cursor.executemany(insert_query, users)


# retrive 
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)


# Whenever we insert data, we have to tell the connection to actually save all of our change into the data.db file. The way we do that is by doing connection.commit.
connection.commit()

# close conncection after you finish your sql tasks
connection.close()