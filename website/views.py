from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html", user=current_user)