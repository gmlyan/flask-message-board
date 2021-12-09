from server.extensions import ma
from marshmallow import fields
from server.message_board import models
from server.mixins.serializers import CreateMixin
from server.message_board.mixins.validators import EmailValidatorMixin
from server.message_board.mixins.validators import UserValidatorMixin
from server.message_board.mixins.validators import PostValidatorMixin


class UserSerializer(ma.SQLAlchemyAutoSchema, CreateMixin, EmailValidatorMixin):
    class Meta:
        model = models.User

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)


class UserUpdateSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.User

    id = fields.Integer(dump_only=True)
    username = fields.String(required=False)
    email = fields.Email(required=False, dump_only=True)


class PostSerializer(ma.SQLAlchemyAutoSchema, CreateMixin, UserValidatorMixin):
    class Meta:
        model = models.Post
        include_fk = True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    edited_at = fields.DateTime(dump_only=True)


class PostUpdateSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Post
        include_fk = True

    id = fields.Integer(dump_only=True)
    headline = fields.String(required=False)
    content = fields.String(required=False)
    user_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    edited_at = fields.DateTime(dump_only=True)


class CommentSerializer(ma.SQLAlchemyAutoSchema, CreateMixin, UserValidatorMixin, PostValidatorMixin):
    class Meta:
        model = models.Comment
        include_fk = True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    edited_at = fields.DateTime(dump_only=True)


class CommentUpdateSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Comment
        include_fk = True

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    post_id = fields.Integer(dump_only=True)
    content = fields.String(required=False)
    created_at = fields.DateTime(dump_only=True)
    edited_at = fields.DateTime(dump_only=True)


user_serializer = UserSerializer()
user_update_serializer = UserUpdateSerializer()
post_serializer = PostSerializer()
post_update_serializer = PostUpdateSerializer()
comment_serializer = CommentSerializer()
comment_update_serializer = CommentUpdateSerializer()

