from app.extensions import db, ma
from app.models import Post


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        sqla_session = db.session
        include_fk = True


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
