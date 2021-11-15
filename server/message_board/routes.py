from . import views


def register_routes(api):
    api.add_resource(views.UserView, '/users/', '/users/<int:user_id>/')
