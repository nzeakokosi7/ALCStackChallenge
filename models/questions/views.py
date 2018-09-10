from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.users.views import token_required
from models.questions.questions import Question

question_blueprint = Blueprint('question_view', __name__)


@question_blueprint.route('/questions', methods=['GET', 'POST'])
@token_required
def questions(current_user):
    blank_title = ""
    blank_question = ""
    if request.method == 'POST':
        title = request.form['title']
        asked_question = request.form['asked_question']

        if title == blank_title or asked_question == blank_question:
            if title == "":
                blank_title += "This field is empty"
            if asked_question == "":
                blank_question += "This field is empty"
            return render_template('question_view/create_question.html',
                                   title='New Question',
                                   current_user=current_user,
                                   blank_question=blank_question,
                                   blank_title=blank_title)

        if title == blank_title and asked_question == blank_question:
            blank_title += "This field is empty"
            blank_question += "This field is empty"
            return render_template('question_view/create_question.html',
                                   title='New Question',
                                   current_user=current_user,
                                   blank_question=blank_question,
                                   blank_title=blank_title)

        new_question = Question(user_id=current_user.public_id, title=title, question=asked_question)
        print("user_id", new_question.user_id)
        print("time" + new_question.question_timestamp)
        print("date" + new_question.asked_date)
        print("title" + new_question.question_title)
        print("text" + new_question.question_text)
        new_question.save_to_db()
        flash('Your Question has been asked, wait for answers!', 'success')
        return redirect(url_for('users_view.profile'))

    return render_template('question_view/create_question.html',
                           title='New Question',
                           current_user=current_user,
                           blank_question=blank_question,
                           blank_title=blank_title)
