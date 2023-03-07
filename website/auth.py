from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return f"Login"

@auth.route("/logout")
def logout():
    return f"Logout"

@auth.route("/sign-up")
def sign_up():
    return f"Sign Up"