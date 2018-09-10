import datetime
import sqlite3

from models.questions.questions import Question


class Answers(object):
    date_time = str(datetime.datetime.utcnow()).split()
    date, time = date_time
    time = time.split(".")
    time = time[0]

    question_attrib = Question()
    question_id = question_attrib.question_id
    user_id_fom_question = question_attrib.user_id

    def __init__(self, answer_id=None, question_id=question_id, user_id=user_id_fom_question,
                 timestamp=time, date=date, answer=None):
        self.answer_id = answer_id
        self.question_id = question_id
        self.user_id = user_id
        self.answer_text = answer
        self.answer_timestamp = timestamp
        self.answer_date = date

    def get_question(self, _id):
        self.question_id = _id
        que = Question.get_question_by_id(self.question_id)
        if que:
            return que.question_title, que.question_text, que.asked_date, que.question_timestamp
            # question_title = que.question_title
            # question_text = que.question_text
            # asked_date = que.asked_date
            # question_timestamp = que.question_timestamp
            # user_id = que.user_id
            # print("Title: {}\nQuestion: {}\nDate asked: {}\nTime asked: {}-UTC".format(question_title,
            #                                                                            question_text,
            #                                                                            asked_date,
            #                                                                            question_timestamp))
        else:
            return None
            # print("Question with that id {} cannot be found".format(self.question_id))
        # return que.question_title, que.question_text, que.asked_date, que.question_timestamp if que is not None

    @classmethod
    def get_answer(cls, ans_id, que_id):
        connection = sqlite3.connect('./database/stacklite.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM answers where answer_id=? and question_id=?"
        result = cursor.execute(select_query, (ans_id, que_id,))
        row_result = result.fetchone()
        if row_result:
            answer_result = cls(*row_result)
        else:
            answer_result = None
        return answer_result

    def answer_question(self, _id=None, answer_text=None):
        global answer_text_
        answer_text_ = answer_text
        _id = input("Pick a question by id: ")
        self.question_id = int(_id)
        que = Question.get_question_by_id(self.question_id)
        if que is not None:
            question_text = que.question_text
            self.user_id = que.user_id
            print("Question: {}".format(question_text))
            answer_text_ = input("Type your answer here: ")
            print("answer for question: {}\nAnswer {}".format(question_text, answer_text_))
            Answers.save_to_db(self, self.user_id, self.question_id, answer_text_)
        else:
            print("Question with that id {} cannot be found".format(self.question_id))

    def get_all_answers_to_a_question(self, _id):
        que_id = Answers.get_question(self, _id)
        total_questions_by_user_id = []
        if que_id is not None:
            _, param_1, _, _ = que_id
            connection = sqlite3.connect('./database/stacklite.db')
            cursor = connection.cursor()

            query = "SELECT answers FROM answers WHERE question_id=?"
            result = cursor.execute(query, (int(_id),))
            row = result.fetchall()
            if row:
                for ans in row:
                    total_questions_by_user_id.append(list(ans))
                print("Showing all answers to question:\n{}\n================".format(param_1))
                for ans_given in total_questions_by_user_id:
                    for ans in ans_given:
                        print(ans)
            else:
                print("Showing all answers to question:\n{}\n================".format(param_1))
                print("No answers found".format(_id))
            connection.close()
        else:
            print("Question id ({}) cannot be found!".format(_id))

    def save_to_db(self, user_id, _id, answer_text):
        connection = sqlite3.connect('./database/stacklite.db')
        cursor = connection.cursor()

        query = "INSERT INTO answers VALUES (NULL, ?, ?, ?, ?, ?)"
        cursor.execute(query, (_id, user_id,
                               self.answer_timestamp, self.answer_date, answer_text))
        connection.commit()
        connection.close()
        return "Answers Saved"

    def display_questions_and_answer(self, que_id, ans_id):
        param_1 = Answers.get_question(self, que_id)
        # if Answers.get_question(self, que_id):
        #     _, param_1, _, _ = Answers.get_question(self, que_id)
        # else:
        #     return m
        #     print("Question id ({}) cannot be found!".format(que_id))

        if param_1 is not None:
            _, param_1, _, _ = Answers.get_question(self, que_id)

        param_2 = Answers.get_answer(ans_id, que_id)

        if param_1 and param_2:
            print("Question: {}, Answer: {}".format(param_1, param_2.answer_text))
        elif param_1 is None and param_2:
            print("Question id ({}) cannot be found!".format(que_id))
        elif param_2 is None and param_1:
            print("Answer id ({}) cannot be found!".format(ans_id))
        else:
            print("Nothing found!, both ID's are wrong")

#
#     @staticmethod
#     def get_all_answers_in_db():
#         connection = sqlite3.connect('stacklite.db')
#         cursor = connection.cursor()
#         select_query = "SELECT * FROM questions"
#         result = cursor.execute(select_query)
#
#         total_answers_in_db = []
#         if result:
#             for rows in result:
#                 total_answers_in_db.append(rows)
#         else:
#             print("Question not found")
#         connection.close()
#         for total in total_answers_in_db:
#             print(total)
#         return total_answers_in_db
#
#     @classmethod
#     def get_question_by_id(cls, _id):
#         connection = sqlite3.connect('stacklite.db')
#         cursor = connection.cursor()
#
#         select_query = "SELECT * FROM questions where question_id=?"
#         result = cursor.execute(select_query, (_id,))
#         row_result = result.fetchone()
#         if row_result:
#             question_result = cls(*row_result)
#             print("Question with an ID ({}) found".format(_id))
#             print("Question Title: {}\n"
#                   "Question: {}\n"
#                   "Date created: {}\n"
#                   "Time: {}\n"
#                   "Asked_id: {}\n"
#                   "Question_id: {}".format(question_result.question_title,
#                                            question_result.question_text,
#                                            question_result.asked_date,
#                                            question_result.question_timestamp,
#                                            question_result.user_id,
#                                            question_result.question_id))
#         else:
#             question_result = None
#             print("Question with an ID ({}) not found".format(_id))
#         connection.close()
#         return question_result
#
#     @classmethod
#     def get_all_questions_by_user_id(cls, _id):
#         connection = sqlite3.connect('stacklite.db')
#         cursor = connection.cursor()
#
#         select_query = "SELECT * FROM questions where user_id=?"
#         result = cursor.execute(select_query, (_id,))
#         total_questions_by_user_id = []
#         if result:
#             print("Question with an ID ({}) found".format(_id))
#             print(result)
#             for ans in result:
#                 list_ans = cls(*list(ans))
#                 total_questions_by_user_id.append(list_ans)
#                 print("Question Title: {}\n"
#                       "Question: {}\n"
#                       "Date created: {}\n"
#                       "Time: {}\n"
#                       "Asked_id: {}\n"
#                       "Question_id: {}\n"
#                       "======================\n".format(list_ans.question_title,
#                                                         list_ans.question_text,
#                                                         list_ans.asked_date,
#                                                         list_ans.question_timestamp,
#                                                         list_ans.user_id,
#                                                         list_ans.question_id))
#
#         connection.close()
#         if total_questions_by_user_id is None:
#             print("Question with an ID ({}) not found".format(_id))
#         return total_questions_by_user_id
#
#     @staticmethod
#     def delete_question(_id):
#         connection = sqlite3.connect('stacklite.db')
#         cursor = connection.cursor()
#
#         select_query = "SELECT question_id FROM questions where question_id=?"
#         result = cursor.execute(select_query, (_id,))
#         row = result.fetchone()
#         if row is None:
#             print("ID not found or has been previously deleted!")
#         else:
#             query = "DELETE FROM questions WHERE question_id=?"
#             cursor.execute(query, (_id,))
#             print("question id with id number ({}) deleted".format(_id))
#         connection.commit()
#         connection.close()
#         return "Question Saved"
#
#
# # new_User = Question(20, title="Batteries", question="What are the best batteries out there?")
# # new_User.save_to_db()
# #
# # new_user_2 = Question(user_id=300, title="Fruits", question="Are paw-paw fruits?")
# # new_user_2.save_to_db()
# # Question.get_all_questions_by_user_id(50)
# Question.get_all_questions_in_db()
# # print(new_User.time)


if __name__ == "__main__":
    new_ans = Answers()
    # new_ans.answer_question()
    new_ans.get_all_answers_to_a_question(5)
