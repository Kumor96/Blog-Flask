from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts = posts)

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash("Posts cannot be empty", category='error')
        else:
            post = Post(text=text, author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category='success')
            return redirect(url_for('views.home'))
    return render_template("create_post.html", user=current_user)

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No user with that username", category='error')

    posts = user.posts

    return render_template("posts.html", user=current_user, posts=posts, username=user.username)