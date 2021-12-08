from http import HTTPStatus
from flask_restful import Resource


class TestConnection(Resource):

    def get(self):
        return {'Ping': 'Pong'}, HTTPStatus.OK
