from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from flask_restful import Resource
from webargs.flaskparser import use_args
from sqlalchemy import exc
from . import models
from .serializers import user_serializer
from .serializers import user_update_serializer


class UserView(Resource):

    model = models.User

    def get(self, user_id=None):
        print(request.method)
        if user_id:
            user = self.model.query.filter_by(id=user_id).first()
            if not user:
                abort(404)
            return jsonify(user.serialize())
        users = self.model.query.all()
        return jsonify([user.serialize() for user in users])

    @use_args(user_serializer)
    def post(self, args):
        try:
            user = user_serializer.save(args)
            return make_response(jsonify(user.serialize()), 201)
        except exc.IntegrityError:
            return {'message': 'Bad data', 'status': 'fail'}, 400

    @use_args(user_update_serializer)
    def put(self, args, user_id):
        user = self.model.query.filter_by(id=user_id).first()
        if not user:
            abort(404)
        user.update(args)
        return make_response(jsonify(user.serialize()), 200)

    def delete(self, user_id):
        user = self.model.query.filter_by(id=user_id).first()
        if not user:
            abort(404)
        user.destroy()
        return {'message': 'No content'},  204
