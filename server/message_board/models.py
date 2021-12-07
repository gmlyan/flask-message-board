from sqlalchemy.orm import backref
from server.extensions import db
from server.generic.models import Model
from datetime import datetime


class User(Model):
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120))
    age = db.Column(db.Integer)


class Post(Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=backref('posts', cascade='all, delete-orphan'))
    headline = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())


class Comment(Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=backref('comments', cascade='all, delete-orphan'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', backref=backref('comments', cascade='all, delete-orphan'))
    content = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    edited_at = db.Column(db.DateTime, onupdate=datetime.now())
