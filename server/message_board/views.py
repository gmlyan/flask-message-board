from server.message_board import serializers
from server.message_board import models
from server.generic.views import GenericView
from server.mixins import views as view_mixins


# validate id arg existence in methods
class UserView(GenericView, view_mixins.CRUDMixin):

    model = models.User
    serializer = serializers.user_serializer
    serializers = {
        'put': serializers.user_update_serializer
    }


class PostView(GenericView, view_mixins.CRUDMixin):

    model = models.Post
    serializer = serializers.post_serializer
    serializers = {
        'put': serializers.post_update_serializer
    }


class CommentView(GenericView, view_mixins.CRUDMixin):

    model = models.Comment
    serializer = serializers.comment_serializer
    serializers = {
        'put': serializers.comment_update_serializer
    }
