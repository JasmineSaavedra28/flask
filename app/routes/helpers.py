from flask import abort

from app.config import db
from app.models import Post, User


def get_user_or_404(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404, f"User with id {user_id} not found")
    return user


def get_post_or_404(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404, f"Post with id {post_id} not found")
    return post
