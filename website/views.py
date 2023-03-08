from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Post, User, Comment
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

@views.route("/delete-post/<post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)

    if post:
        if post.author != current_user.id:
            flash("You dont have promise", category='error')
        else:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted!",category='success')
            return redirect(url_for('views.home'))
    else:
        flash("Post not found", category='error')
        return redirect(url_for('views.home'))


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))
