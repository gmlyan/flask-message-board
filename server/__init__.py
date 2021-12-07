from http import HTTPStatus
from flask import Flask, jsonify
from flask_restful import Api
from server.message_board.routes import register_routes
from server.extensions import db
from server.extensions import ma
from server.extensions import migrate
from marshmallow import ValidationError


def create_app():
    app = Flask(__name__)
    app.config.from_object('server.config.BaseConfig')
    api = Api(app, prefix='/api/v1')
    register_extenstions(app)
    register_routes(api)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return error.messages, HTTPStatus.BAD_REQUEST

    return app


def register_extenstions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
