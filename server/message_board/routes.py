from server.message_board import views
from server.message_board import TestConnection


def register_routes(api):
    api.add_resource(TestConnection, '/ping/')
    api.add_resource(views.UserView, '/users/', '/users/<int:id>/')
    api.add_resource(views.PostView, '/posts/', '/posts/<int:id>/')
    api.add_resource(views.CommentView, '/comments/', '/comments/<int:id>/')
