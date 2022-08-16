from os import error
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
@auth.route("/", methods=['GET', 'POST'])
def login():

    if request.method == "GET" and current_user.is_authenticated:
        return redirect(url_for("views.home"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        print(user)

        if user and check_password_hash(user.password, password):
            flash('You are logged in!')
            login_user(user, remember=True)
            session.permanent = True
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect e-mail or password!', category='error')

    return render_template("login.html")


@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():

    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            flash('Such email is already registered!', category="error")
        elif password1 != password2:
            flash('Passwords don\'t match', category="error")
        elif len(email) < 11:
            flash('Email address is too short', category="error")
        elif len(password1) < 8:
            flash(
                'Password is too short, please use at least 8 characters', category="error")
        else:
            new_user = User(email=email, firstname=firstname,
                            lastname=lastname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created successfully!', category='info')
            return redirect(url_for("views.home"))

    return render_template("sign-up.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()
    flash('You are logged out successfully!', category='info')
    return redirect(url_for("auth.login"))
