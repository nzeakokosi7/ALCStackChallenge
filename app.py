import jwt
from flask import Flask, render_template, session

from models.users.user import User
from models.users.views import user_blueprint
from models.questions.views import question_blueprint

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
@app.route('/home')
def home():
    token = None
    current_user = None
    if 'x-access-token' in session:
        token = session.get('x-access-token')
    if token:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        current_user = User.find_by_id(_id=data['public_id'])
    return render_template('users_view/about.html', current_user=current_user)


app.register_blueprint(user_blueprint)
app.register_blueprint(question_blueprint)
