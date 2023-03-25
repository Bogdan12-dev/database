import datetime
from flask import render_template, request,redirect,url_for, get_flashed_messages, flash
from .forms import LoginForm,SignupForm
from werkzeug.security import generate_password_hash, check_password_hash
from api.database import session
from flask_login import login_user
from api.communicate_with_db import get_user_by_nickname, add_item_to_db
from . import app, weather_api
@app.route("/")
@app.route("/main")
def main():
    weather = weather_api.get_weather("Sumy")
    date = datetime.datetime.now().date().strftime("%d/%m/%Y")
    return render_template("main.html", weather=weather)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm
    if request.method == "POST":
        user = get_user_by_nickname(form.nickname.data)
        if user:
            is_password_correct = check_password_hash(user.password, form.password.data)
            if is_password_correct:
                login_user(user)
                return redirect("main")
            flash("u might entered wrong password")
        flash("there is no user with such name")
        return redirect("login")
    return render_template("login.html", form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm
    if request.method == "POST":
        user = get_user_by_nickname(form.nickname.data)
        if user:
            flash("this user already exists")
            return redirect("signup")
        password = generate_password_hash(form.password.data)
        user = User(nickname=form.nickname.data, email=form.email.data, password=password)
        add_item_to_db(user)
        return redirect("login")
    return render_template("signup.html", form=form)

@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(405)
def handle_error(error):
    return render_template("error_page.html", code=error.code)
