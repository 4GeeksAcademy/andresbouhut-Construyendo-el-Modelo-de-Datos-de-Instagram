from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    profile_picture: Mapped[str] = mapped_column(String(250), nullable=True)

    posts: Mapped[list['Post']] = relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    following: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys='Follower.user_id',
        back_populates='follower_user',
        cascade='all, delete-orphan'
    )

    followers: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys='Follower.user_to_id',
        back_populates='followed_user',
        cascade='all, delete-orphan'
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture
        }

class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship('User', back_populates='posts')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='post', cascade='all, delete-orphan')

class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

class Follower(db.Model):
    __tablename__ = 'follower'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    follower_user: Mapped['User'] = relationship('User', foreign_keys=[user_id], back_populates='following')
    followed_user: Mapped['User'] = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

from eralchemy2 import render_er
render_er(db.Model, 'diagram.png')
