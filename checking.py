# # import sqlite3
# # connection = sqlite3.connect('./database/Credentials.db')
# # cursor = connection.cursor()
# #
# # query = "SELECT * FROM users_credential ORDER BY username ASC "
# # result = cursor.execute(query, )
# # rows = result.fetchall()
# # new_username = []
# # new_email = []
# # for row in rows:
# #     new_username.append(row[1])
# #     new_email.append(row[2])
# # print(new_email)
# # # print(new_username)
#
# picture = "mice.jar.jpg"
# strip_picture = picture.split(".")[-1]
# if strip_picture != "jpg" or strip_picture != "png":
#     print("FIle type not allowed")
# else:
#     print()
# print(strip_picture)
from models.questions.questions import Question

new_user_2 = Question(user_id=300, title="Fruits", question="Whats the essence of eating an Apple")
new_user_2.save_to_db()
