from flask import Flask, render_template, request, session

from src.common.database import Database
from src.models.user import User

app = Flask(__name__)
app.secret_key = "BENC"


@app.route('/')
def hello_template():
    return render_template('home.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/login') # www.mysite.com./api/register
def login_template():
    return render_template('login.html')


@app.route('/register') # www/mysite.com/api/register
def register_template():
    return render_template('register.html')


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)

    return render_template("profile.html", email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("profile.html", email=session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        # print("@ Not None")
        user = User.get_by_id(user_id)
    else:
        # print("@ None")
        # print("Email: {}".format(session['email']))
        user = User.get_by_email(session['email'])
        # print("User: {}".format(user))
    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)


if __name__ == "__main__":
    app.run()