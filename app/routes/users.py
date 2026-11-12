from flask import abort

from app.extensions import db
from app.models import User
from app.routes.helpers import get_user_or_404
from app.schemas import user_schema, users_schema


def read_all():
    users = User.query.order_by(User.username).all()
    return users_schema.dump(users)


def create(user):
    username = (user.get("username") or "").strip()
    email = (user.get("email") or "").strip()

    if not username:
        abort(400, "Field 'username' is required")
    if not email:
        abort(400, "Field 'email' is required")

    existing_user = User.query.filter(User.username == username).one_or_none()
    if existing_user is not None:
        abort(406, f"User with username {username} already exists")

    user["username"] = username
    user["email"] = email
    new_user = user_schema.load(user, session=db.session)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201


def read_one(user_id):
    user = get_user_or_404(user_id)
    return user_schema.dump(user)


def update(user_id, user):
    existing_user = get_user_or_404(user_id)

    update_user = user_schema.load(user, session=db.session)
    username = (update_user.username or "").strip()
    email = (update_user.email or "").strip()

    if not username:
        abort(400, "Field 'username' is required")
    if not email:
        abort(400, "Field 'email' is required")

    duplicate = User.query.filter(
        User.username == username,
        User.id != user_id,
    ).one_or_none()
    if duplicate is not None:
        abort(406, f"User with username {username} already exists")

    existing_user.username = username
    existing_user.email = email

    db.session.commit()
    return user_schema.dump(existing_user), 200


def delete(user_id):
    existing_user = get_user_or_404(user_id)

    # cascade="all, delete-orphan" elimina también todos sus posts.
    db.session.delete(existing_user)
    db.session.commit()
    return "", 204
