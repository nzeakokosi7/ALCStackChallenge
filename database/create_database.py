import sqlite3

connection = sqlite3.connect('Credentials.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users_credential (id INTEGER PRIMARY KEY," \
                                                           " username text," \
                                                           " email text,"\
                                                           " password text," \
                                                           " public_id text," \
                                                           "profile_picture text)"
cursor.execute(create_table)

# create_table = "CREATE TABLE IF NOT EXISTS users_credential_test (name text, price real)"
# cursor.execute(create_table)

connection.commit()
connection.close()
