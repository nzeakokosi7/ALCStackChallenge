import sqlite3
import uuid


class User:
    def __init__(self, inc_id=None, username=None, email=None, password=None, public_id=None, default_image=None):
        self.inc_id = inc_id
        self.username = username
        self.email = email
        self.password = password
        self.public_id = uuid.uuid4().__str__() if public_id is None else public_id
        self.default_image = "default.png" if default_image is None else default_image

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('./database/Credentials.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users_credential WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)  # same as row[0], row[1], row[2]...passing args by position
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_email(cls, email):
        connection = sqlite3.connect('./database/Credentials.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users_credential WHERE email=?"
        result = cursor.execute(query, (email,))
        row = result.fetchone()
        if row:
            user = cls(*row)  # same as row[0], row[1], row[2]...passing args by position
        else:
            user = None

        connection.close()
        return user

    @staticmethod
    def find_all_emails_and_usernames():
        connection = sqlite3.connect('./database/Credentials.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users_credential ORDER BY email ASC "
        result = cursor.execute(query, )
        rows = result.fetchall()
        new_username = []
        new_email = []
        for row in rows:
            new_username.append(row[1])
            new_email.append(row[2])
        return new_username, new_email

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('./database/Credentials.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users_credential WHERE public_id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)  # same as row[0], row[1], row[2]...passing args by position
        else:
            user = None

        connection.close()
        return user


# class UserRegistration(Resource):
#
#     parser = reqparse.RequestParser()
#     parser.add_argument('username',
#                         type=str,
#                         required=True,
#                         help="This field cannot be blank.")
#     parser.add_argument('password',
#                         type=str,
#                         required=True,
#                         help="This field cannot be blank.")
#
#     @staticmethod
#     def post():
#         data = UserRegistration.parser.parse_args()
#         if User.find_by_username(data['username']):
#             return {"message": "A user with that username ({}) already exists".format(data['username'])}
#
#         connection = sqlite3.connect('./database/Credentials.db')
#         cursor = connection.cursor()
#
#         query = "INSERT INTO users_credential VALUES (NULL, ?, ?)"
#         cursor.execute(query, (data['username'], data['password'],))
#
#         connection.commit()
#         connection.close()
#
#         return {"message": "User Created successfully with username {}".format(data['username'])}, 201

# user = User.encode_auth_token("125bebb8-a71b-4e26-aa6c-9b77f95786de")
# print(user)
