from http import HTTPStatus
from flask import request


class CreateModelMixin:

    def post(self):
        json_data = request.get_json()
        serializer = self.get_serializer('post')
        validated_data = serializer.load(json_data)
        instance = serializer.create(validated_data)
        return instance, HTTPStatus.CREATED


class RetrieveModelMixin:

    def get(self, id=None):
        serializer = self.get_serializer('get')
        if id:
            instance = self.get_instance(id)
            result = serializer.dump(instance)
        else:
            instances = self.get_queryset()
            result = serializer.dump(instances, many=True)
        return result, HTTPStatus.OK


class UpdateModelMixin:

    def put(self, id):
        json_data = request.get_json()
        serializer = self.get_serializer('put')
        validated_data = serializer.load(json_data)
        instance = self.get_instance(id)
        instance.update(validated_data)
        return serializer.dump(instance), HTTPStatus.OK


class DeleteModelMixin:

    def delete(self, id):
        serializer = self.get_serializer('delete')
        instance = self.get_instance(id)
        instance.destroy()
        return serializer.dump(instance), HTTPStatus.OK


class CRUDMixin(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DeleteModelMixin):
    pass
