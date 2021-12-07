from http import HTTPStatus
from flask_restful import Resource, abort


class GenericView(Resource):

    model = None
    serializer = None
    serializers = {
        'get': serializer,
        'post': serializer,
        'put': serializer,
        'delete': serializer
    }

    def get_queryset(self):
        return self.model.query.all()

    def get_instance(self, instance_id):
        instance = self.model.query.filter_by(id=instance_id).first()
        if not instance:
            abort(HTTPStatus.NOT_FOUND)
        return instance

    def get_serializer(self, method=None):
        if not method:
            return self.serializer
        assert method in ['get', 'post', 'put', 'delete'], 'Ivalid action. Available actions: (get, post, put, delete)'
        return self.serializers.get(method) or self.serializer
