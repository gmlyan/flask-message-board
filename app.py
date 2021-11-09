from flask import Flask
from flask_restful import Api
from server.config import BaseConfig
from server.extensions import db
from server.extensions import ma
from server.extensions import migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object('server.config.BaseConfig')
    api = Api(app, prefix='/api/v1')
    register_extenstions(app)
    return app


def register_extenstions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)


application = create_app()

if __name__ == '__main__':
    application.run(host=BaseConfig.HOST, port=BaseConfig.PORT)
