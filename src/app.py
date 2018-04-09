from flask import Flask, render_template, request, session

from src.common.database import Database
from src.models.user import User

app = Flask(__name__)
app.secret_key = "BENC"


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    print("@login_user {} , {}".format(email, password))
    if User.login_valid(email, password):
        print("@ user_login_valid")
        User.login(email)

    return render_template("profile.html", email=session['email'])


if __name__ == "__main__":
    app.run()