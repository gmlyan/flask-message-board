from server.message_board import models
from marshmallow import validates_schema
from marshmallow import ValidationError


class EmailValidatorMixin:

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get('email')
        if models.User.query.filter_by(email=email).first():
            raise ValidationError('Email is already taken')


class UserValidatorMixin:

    @validates_schema
    def validate_user(self, data, **kwargs):
        user_id = data.get('user_id')
        if not models.User.query.filter_by(id=user_id).first():
            raise ValidationError('User does not exist')


class PostValidatorMixin:

    @validates_schema
    def validate_post(self, data, **kwargs):
        post_id = data.get('post_id')
        if not models.Post.query.filter_by(id=post_id).first():
            raise ValidationError('Post does not exist')