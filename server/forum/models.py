from server.extensions import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120))
    age = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    headline = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<Publication %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    edited = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return '<Comment %r>' % self.id
