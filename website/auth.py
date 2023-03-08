from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Welcome", category='success')
                redirect(url_for('views.home'))
            else:
                flash('Passwords incorrect!', category='error')
        else:
            flash("User doesn't exist", category='error')
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are log out",category='success')
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("Email already in use", category='error')
        elif username_exists:
            flash("Username is already exists", category='error')
        elif password1 != password2:
            flash("Passwords dont match", category='error')
        elif len(username) < 2:
            flash("Username is too short", category='error')
        elif len(password1) < 6:
            flash("Password is too short", category='error')
        elif len(email) < 6:
            flash("Email is invalid", category='error')
        else:
            new_user = User(email=email, username=username, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Welcome!", category='success')
            login_user(new_user, remember=True)
    return render_template("sign_up.html", user=current_user)