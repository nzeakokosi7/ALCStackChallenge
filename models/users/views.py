import os
import sqlite3
import jwt
import app
import secrets
from PIL import Image
from flask import Blueprint, request, session, render_template, redirect, url_for, make_response, flash
from werkzeug.security import safe_str_cmp
from functools import wraps

from models.questions.questions import Question
from models.users.user import User
from utils import Utils

user_blueprint = Blueprint('users_view', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in session:
            token = session.get('x-access-token')
        if not token:
            # return redirect(url_for(".login_user"))
            return redirect(url_for("users_view.login_user"))
        try:
            data = jwt.decode(token, app.app.config['SECRET_KEY'])
            current_user = User.find_by_id(_id=data['public_id'])
        except:
            return redirect(url_for("users_view.login_user"))
        return f(current_user, *args, **kwargs)

    return decorated


@user_blueprint.route('/auth/login', methods=['GET', 'POST'])
def login_user():
    global token_login
    current_user_logged = None
    token = None
    blank_username = ""
    blank_password = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.find_by_username(username=username)

        if username == blank_username and password == blank_password:
            blank_username += "This Field Is Required!"
            blank_password += "This Field Is Required!"
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template("users_view/login.html",
                                                 current_user=current_user_logged,
                                                 blank_password=blank_password,
                                                 blank_username=blank_username), 200, headers)

        if username == blank_username or password == blank_password:
            if username == "":
                blank_username += "This Field Is Required!"
            if password == "":
                blank_password += "This Field Is Required!"
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template("users_view/login.html",
                                                 blank_password=blank_password,
                                                 current_user=current_user_logged,
                                                 blank_username=blank_username), 200, headers)

        if user and Utils.check_encrypted_password(password, user.password):
            token_login = jwt.encode({'public_id': user.public_id},
                                     app.app.config['SECRET_KEY'])
            session['x-access-token'] = token_login.decode('UTF-8')
            flash('You have been logged in!', 'success')
            header = {'Content-Type': 'text/html'}
            return make_response(redirect(url_for(".profile")), header)
        else:
            flash('Login Failed. Please check if username and password are correct!', 'danger')
    if 'x-access-token' in session:
        token = session.get('x-access-token')
    if token:
        data = jwt.decode(token, app.app.config['SECRET_KEY'])
        current_user_logged += User.find_by_id(_id=data['public_id'])
        header = {'Content-Type': 'text/html'}
        return make_response(redirect(url_for(".profile")), header)
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template("users_view/login.html",
                                         current_user=current_user_logged,
                                         blank_password=blank_password,
                                         blank_username=blank_username), 200, headers)


@user_blueprint.route('/auth/signup', methods=['GET', 'POST'])
def register_user():
    global token_login
    token = None
    current_user = None
    blank_mail = ""
    blank_password = ""
    blank_username = ""
    blank_confirm_password = ""

    if request.method == 'POST':
        email_register = request.form['email']
        username_register = request.form['username']
        password_register = request.form['password']
        confirm_password = request.form['confirm password']

        username_from_database = User.find_by_username(username=username_register)
        email_from_database = User.find_by_email(email=email_register)

        if email_register == blank_mail and username_register == blank_username and \
                password_register == blank_password and confirm_password == blank_confirm_password:
            blank_mail += "This field is required"
            blank_username += "This field is required"
            blank_password += "This field is required"
            blank_confirm_password += "This field is required"
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template("users_view/register.html", title='Register',
                                                 blank_mail=blank_mail,
                                                 current_user=current_user,
                                                 blank_confirm_password=blank_confirm_password,
                                                 blank_password=blank_password,
                                                 blank_username=blank_username), 200, headers)

        if email_register == blank_mail or username_register == blank_username or \
                password_register == blank_password or confirm_password == blank_confirm_password:
            if email_register == "":
                blank_mail += "This field is required"

            if username_register == "":
                blank_username += "This field is required"

            if password_register == "":
                blank_password += "This field is required"

            if confirm_password == "":
                blank_confirm_password += "This field is required"

            headers = {'Content-Type': 'text/html'}
            return make_response(render_template("users_view/register.html", title='Register',
                                                 current_user=current_user,
                                                 blank_mail=blank_mail,
                                                 blank_confirm_password=blank_confirm_password,
                                                 blank_password=blank_password,
                                                 blank_username=blank_username), 200, headers)
        if username_from_database is None and email_from_database is None and email_register and username_register and password_register and confirm_password:
            if "@" in username_register:
                flash(f"Username cannot contain special characters", 'danger')
                headers = {'Content-Type': 'text/html'}
                # print(blank_password)
                return make_response(render_template("users_view/register.html", title='Register',
                                                     current_user=current_user,
                                                     blank_mail=blank_mail,
                                                     blank_confirm_password=blank_confirm_password,
                                                     blank_password=blank_password,
                                                     blank_username=blank_username), 200, headers)

            if len(username_register) < 3 or len(username_register) > 20:
                print(len(username_register))
                flash(f'Username field must be between 3 and 20 characters long', 'danger')
                headers = {'Content-Type': 'text/html'}
                # print(blank_password)
                return make_response(render_template("users_view/register.html", title='Register',
                                                     current_user=current_user,
                                                     blank_mail=blank_mail,
                                                     blank_confirm_password=blank_confirm_password,
                                                     blank_password=blank_password,
                                                     blank_username=blank_username), 200, headers)

            if safe_str_cmp(password_register, confirm_password):
                encrypted_password = Utils.encrypt_password(password=password_register)
                user_created = User(username=username_register, email=email_register, password=encrypted_password)
                connection = sqlite3.connect('./database/Credentials.db')
                cursor = connection.cursor()

                query = "INSERT INTO users_credential VALUES (NULL, ?, ?, ?, ?, ?)"
                cursor.execute(query, (user_created.username, user_created.email,
                                       user_created.password, user_created.public_id, user_created.default_image))

                connection.commit()
                connection.close()

                user_public_id = User.find_by_username(username=username_register)
                token_login = jwt.encode({'public_id': user_public_id.public_id},
                                         app.app.config['SECRET_KEY'])
                flash(f'Your account has been created! You can now able to log in', 'success')
                return redirect(url_for(".login_user"))
            else:
                headers = {'Content-Type': 'text/html'}
                blank_password += "Field does not match"
                blank_confirm_password += "Field does not match"
                # print(blank_password)
                return make_response(render_template("users_view/register.html", title='Register',
                                                     current_user=current_user,
                                                     blank_mail=blank_mail,
                                                     blank_confirm_password=blank_confirm_password,
                                                     blank_password=blank_password,
                                                     blank_username=blank_username), 200, headers)
        if email_from_database:
            if email_register == email_from_database.email:
                blank_mail += "Email is already registered"
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template("users_view/register.html", title='Register',
                                                     current_user=current_user,
                                                     blank_mail=blank_mail,
                                                     blank_confirm_password=blank_confirm_password,
                                                     blank_password=blank_password,
                                                     blank_username=blank_username), 200, headers)
        if username_from_database:
            if username_register == username_from_database.username:
                blank_username += "Username is already taken!"
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template("users_view/register.html", title='Register',
                                                     current_user=current_user,
                                                     blank_mail=blank_mail,
                                                     blank_confirm_password=blank_confirm_password,
                                                     blank_password=blank_password,
                                                     blank_username=blank_username), 200, headers)
    if 'x-access-token' in session:
        token = session.get('x-access-token')
    if token:
        data = jwt.decode(token, app.app.config['SECRET_KEY'])
        current_user += User.find_by_id(_id=data['public_id'])
        header = {'Content-Type': 'text/html'}
        return make_response(redirect(url_for(".profile")), header)
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template("users_view/register.html", title='Register',
                                         current_user=current_user,
                                         blank_mail=blank_mail,
                                         blank_confirm_password=blank_confirm_password,
                                         blank_password=blank_password,
                                         blank_username=blank_username), 200, headers)


@user_blueprint.route('/logout')
@token_required
def logout_user(current_user):
    session['x-access-token'] = None
    return redirect(url_for("home"))


@user_blueprint.route('/profile')
@token_required
def profile(current_user):
    image_file = url_for('static', filename='assets/pictures/' + current_user.default_image)
    all_questions = Question.get_all_questions_by_user_id(current_user.public_id)
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template("users_view/users_home.html",
                                         title='Profile',
                                         current_user=current_user,
                                         all_questions=all_questions,
                                         image_file=image_file), 200, headers)


@user_blueprint.route('/account', methods=['GET', 'POST'])
@token_required
def user_account(current_user):
    blank_email = ""
    blank_username = ""
    blank_file = ""
    file = None

    if request.method == 'POST':
        email_update = request.form['email']
        username_update = request.form['username']
        try:
            file = request.files['file']
        except Exception:
            pass

        username_from_database = User.find_by_username(username=current_user.username)
        email_from_database = User.find_by_email(email=current_user.email)
        all_username_from_database, all_emails_from_database = User.find_all_emails_and_usernames()

        # if email_update == blank_email and username_update == blank_username:
        #     blank_email += "This field is required"
        #     blank_username += "This field is required"
        #     headers_update = {'Content-Type': 'text/html'}
        #     image_file = url_for('static', filename='assets/pictures/' + current_user.default_image)
        #     return make_response(render_template("users_view/accounts.html", title='Account',
        #                                          image_file=image_file,
        #                                          blank_file=blank_file,
        #                                          current_user=current_user,
        #                                          blank_email=blank_email,
        #                                          blank_username=blank_username), 200, headers_update)

        if file or email_update != blank_email or username_update != blank_username:
            if file:
                if Utils.allowed_file(file.filename):
                    # filename = secure_filename(file.filename)
                    random_hex = secrets.token_hex(8)
                    _, file_ext = os.path.splitext(file.filename)
                    picture_file = random_hex + file_ext
                    output_size = (125, 125)
                    new_img = Image.open(file)
                    new_img.thumbnail(output_size)
                    new_img.save(os.path.join(app.app.config['UPLOAD_FOLDER'], picture_file))
                    current_user.default_image = picture_file
                    connection = sqlite3.connect('./database/Credentials.db')
                    cursor = connection.cursor()

                    query = "UPDATE users_credential SET profile_picture=? WHERE id=?"
                    cursor.execute(query, (picture_file, email_from_database.inc_id,))

                    connection.commit()
                    connection.close()
                else:
                    blank_file += "File does not have an approved extension: jpg, jpeg, png"
                    headers_update = {'Content-Type': 'text/html'}
                    image_file = url_for('static', filename='assets/pictures/' + current_user.default_image)
                    return make_response(render_template("users_view/accounts.html", title='Account',
                                                         image_file=image_file,
                                                         blank_file=blank_file,
                                                         current_user=current_user,
                                                         blank_email=blank_email,
                                                         blank_username=blank_username), 200, headers_update)

            if username_update != "":
                if len(username_update) < 3 or len(username_update) > 20:
                    flash(f'Username field must be between 3 and 20 characters long', 'danger')
                    headers_update = {'Content-Type': 'text/html'}
                    image_file = url_for('static', filename='assets/pictures/' + current_user.default_image)
                    return make_response(render_template("users_view/accounts.html", title='Account',
                                                         blank_file=blank_file,
                                                         current_user=current_user,
                                                         image_file=image_file,
                                                         blank_email=blank_email,
                                                         blank_username=blank_username), 200, headers_update)

                if "@" in username_update:
                    flash(f"Username cannot contain special characters", 'danger')
                    headers_update = {'Content-Type': 'text/html'}
                    image_file = url_for('static', filename='assets/pictures/' + current_user.default_image)
                    return make_response(render_template("users_view/accounts.html", title='Account',
                                                         blank_file=blank_file,
                                                         current_user=current_user,
                                                         image_file=image_file,
                                                         blank_email=blank_email,
                                                         blank_username=blank_username), 200, headers_update)
                if username_update not in all_username_from_database:
                    connection = sqlite3.connect('./database/Credentials.db')
                    cursor = connection.cursor()
                    query = "UPDATE users_credential SET username=? WHERE id=?"
                    cursor.execute(query, (username_update, username_from_database.inc_id,))

                    connection.commit()
                    connection.close()
                else:
                    flash(f'Username Already Taken', 'warning')
                    return redirect(url_for(".user_account"))

            if email_update != "":
                if email_update not in all_emails_from_database:
                    connection = sqlite3.connect('./database/Credentials.db')
                    cursor = connection.cursor()

                    query = "UPDATE users_credential SET email=? WHERE id=?"
                    cursor.execute(query, (email_update, email_from_database.inc_id,))

                    connection.commit()
                    connection.close()
                else:
                    flash(f'Email already registered', 'warning')
                    return redirect(url_for(".user_account"))
            flash(f'Your account has been updated!', 'success')
            return redirect(url_for(".user_account"))
    image_file = url_for('static', filename='assets/pictures/' + current_user.default_image)
    return render_template("users_view/accounts.html", current_user=current_user,
                           blank_file=blank_file,
                           title='Account', image_file=image_file,
                           blank_email=blank_email,
                           blank_username=blank_username)
