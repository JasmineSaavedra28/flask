from marshmallow import fields

from app.extensions import db, ma
from app.models import User
from app.schemas.post import PostSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    posts = fields.Nested(PostSchema, many=True)

    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session


user_schema = UserSchema()
users_schema = UserSchema(many=True)
