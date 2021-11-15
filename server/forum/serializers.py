from server.extensions import db
from server.extensions import ma
from marshmallow import fields
from . import models


class UserSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.User

    id = fields.Field(dump_only=True)
    email = fields.Email(required=True)

    @classmethod
    def save(cls, args):
        instance = models.User(**args)
        db.session.add(instance)
        db.session.commit()
        return instance


class UserUpdateSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.User

    id = fields.Field(dump_only=True)
    username = fields.String(required=False)
    email = fields.Email(required=False, dump_only=True)


user_serializer = UserSerializer()
user_update_serializer = UserUpdateSerializer()
