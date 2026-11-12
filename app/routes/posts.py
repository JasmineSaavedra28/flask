from flask import abort

from app.extensions import db
from app.models import Post
from app.routes.helpers import get_post_or_404, get_user_or_404
from app.schemas import post_schema, posts_schema


def read_all():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return posts_schema.dump(posts)


def read_one(post_id):
    post = get_post_or_404(post_id)
    return post_schema.dump(post)


def read_by_user(user_id):
    user = get_user_or_404(user_id)
    return posts_schema.dump(user.posts)


def create(post):
    user_id = post.get("user_id")
    if user_id is None:
        abort(400, "Field 'user_id' is required")

    # Verifica que el usuario exista antes de crear el post.
    get_user_or_404(user_id)

    title = (post.get("title") or "").strip()
    if not title:
        abort(400, "Field 'title' is required")

    post["title"] = title
    new_post = post_schema.load(post, session=db.session)
    db.session.add(new_post)
    db.session.commit()
    return post_schema.dump(new_post), 201


def update(post_id, post):
    existing_post = get_post_or_404(post_id)

    user_id = post.get("user_id", existing_post.user_id)
    get_user_or_404(user_id)

    title = (post.get("title") or existing_post.title).strip()
    if not title:
        abort(400, "Field 'title' is required")

    existing_post.title = title
    existing_post.content = post.get("content", existing_post.content)
    existing_post.user_id = user_id

    db.session.commit()
    return post_schema.dump(existing_post), 200


def delete(post_id):
    existing_post = get_post_or_404(post_id)

    db.session.delete(existing_post)
    db.session.commit()
    return "", 204
