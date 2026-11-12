from flask import Blueprint, render_template

from app.models import Post, User

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    users = User.query.order_by(User.username).all()
    total_posts = Post.query.count()
    return render_template(
        "home.html",
        users=users,
        total_posts=total_posts,
    )
