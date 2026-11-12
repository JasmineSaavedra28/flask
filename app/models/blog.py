from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class User(db.Model):
    """Usuario: lado "uno" de la relación User 1 ---- N Post."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Un usuario tiene muchos posts. Al eliminarlo, sus posts se eliminan
    # en cascada (delete-orphan).
    posts: Mapped[list["Post"]] = db.relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",
        order_by="Post.title",
    )


class Post(db.Model):
    """Artículo: lado "muchos" de la relación User 1 ---- N Post."""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relación inversa: cada post pertenece a un único usuario.
    author: Mapped["User"] = db.relationship("User", back_populates="posts")
