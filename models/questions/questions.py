import datetime
import os
import sqlite3


class Question(object):
    """
    This is the Question class object with defined properties
    """
    date_time = str(datetime.datetime.utcnow()).split()
    date, time = date_time
    date = str(date)
    time = time.split(".")
    time = time[0].__str__()

    def __init__(self, question_id=None, user_id=None, timestamp=time, date=date, title=None, question=None):
        """
            Initializes, the question class with the given parameters
        Args:
            question_id (): The question identifier
            user_id (): The user identifier
            timestamp (): The time the question was created in UTC
            date (): The date the question was created
            title (): Title of the question
            question (): The question content
        """
        self.question_id = question_id
        self.user_id = user_id
        self.question_title = title
        self.question_text = question
        self.question_timestamp = timestamp
        self.asked_date = date

    def save_to_db(self):
        """
        This saves the question to the database
        Returns: A notification string

        """
        connection = sqlite3.connect("./database/stacklite.db")
        cursor = connection.cursor()

        query = "INSERT INTO questions VALUES (NULL, ?, ?, ?, ?, ?)"
        cursor.execute(query, (self.user_id, self.question_timestamp,
                               self.asked_date, self.question_title, self.question_text))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all_questions_in_db(limit):
        """
        THis gets all the question asked on our application from a
        database, with a limit
        Args:
            limit (int): This ia an integer that specifies the maximum
                        limit to load from our database

        Returns: A list of all rows specified in the database

        """
        connection = sqlite3.connect("./database/stacklite.db")
        cursor = connection.cursor()
        select_query = "SELECT * FROM questions LIMIT ?"
        result = cursor.execute(select_query, (limit,))

        total_questions_in_db = []
        if result:
            for rows in result:
                if rows is None:
                    print("Question not found")
                else:
                    total_questions_in_db.append(list(rows))
        connection.close()
        print(total_questions_in_db)
        for total in total_questions_in_db:
            print(total)
        return total_questions_in_db

    @classmethod
    def get_question_by_id(cls, _id):
        """
        This gets a question from a question identifier used to tag a particular question,
         it is independent of the identifier.
        Args:
            _id (): This ia an integer for an identifier of a particular question

        Returns: Our base class object (Questions) with the __init__ params.

        """
        connection = sqlite3.connect("./database/stacklite.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM questions where question_id=?"
        result = cursor.execute(select_query, (_id,))
        row_result = result.fetchone()
        if row_result:
            question_result = cls(*row_result)
            # print("Question with an ID ({}) found".format(_id))
            # print("Question Title: {}\n"
            #       "Question: {}\n"
            #       "Date created: {}\n"
            #       "Time: {}\n"
            #       "Asked_id: {}\n"
            #       "Question_id: {}".format(question_result.question_title,
            #                                question_result.question_text,
            #                                question_result.asked_date,
            #                                question_result.question_timestamp,
            #                                question_result.user_id,
            #                                question_result.question_id))
        else:
            question_result = None
            # print("Question with an ID ({}) not found".format(_id))
        connection.close()
        return question_result

    @classmethod
    def get_all_questions_by_user_id(cls, _id):
        """
        This gets all Questions asked from a particular user identity (ID)
        Args:
            _id (): This is the user identifier

        Returns: This returns a list of questions asked by a user with his unique identifier

        """
        connection = sqlite3.connect("./database/stacklite.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM questions where user_id=?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchall()
        total_questions_by_user_id = []

        if row:
            for ans in row:
                if ans:
                    list_ans = cls(*list(ans))
                    total_questions_by_user_id.append({"title": list_ans.question_title,
                                                       "question": list_ans.question_text,
                                                       "date": list_ans.asked_date,
                                                       "time": list_ans.question_timestamp,
                                                       "user_id": list_ans.user_id,
                                                       "question_id": list_ans.question_id})
                # else:
                #     print(total_questions_by_user_id)
                #     print("No questions")
                #     return "No questions Asked"
        else:
            return
        connection.close()
        return total_questions_by_user_id

    @staticmethod
    def delete_question(question_id, user_id):
        """
        This in turns, deletes a question asked by a user, this can only be deleted
        when the user_id matches the question_id
        Args:
            question_id (): an integer that specifies the valid question id
            user_id (): an integer thst specifies the valid user_id

        Returns: A string

        """
        connection = sqlite3.connect("./database/stacklite.db")
        cursor = connection.cursor()

        select_query = "SELECT question_id FROM questions where question_id=?"
        result = cursor.execute(select_query, (question_id, user_id,))
        row = result.fetchone()
        if row is None:
            print("ID not found or has been previously deleted!")
        else:
            query = "DELETE FROM questions WHERE question_id=? AND user_id=?"
            cursor.execute(query, (question_id, user_id,))
            print("question id with id number ({}) deleted".format(question_id))
        connection.commit()
        connection.close()
        return "Question Deleted"
