import sqlite3

connection = sqlite3.connect('stacklite.db')
cursor = connection.cursor()

create_question_table = "CREATE TABLE IF NOT EXISTS questions " \
                        "(question_id INTEGER PRIMARY KEY," \
                        " user_id INTEGER,"\
                        " question_timestamp text," \
                        " question_date text," \
                        " title text," \
                        " questions text)"
cursor.execute(create_question_table)

create_answer_table = "CREATE TABLE IF NOT EXISTS answers"\
                      "(answer_id INTEGER PRIMARY KEY,"\
                      " question_id INTEGER,"\
                      " user_id_from_question INTEGER,"\
                      " answer_timestamp text," \
                      " answer_date text,"\
                      " answers text)"
cursor.execute(create_answer_table)

connection.commit()
connection.close()
