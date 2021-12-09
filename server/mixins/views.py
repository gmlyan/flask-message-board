from http import HTTPStatus
from flask import request


class CreateModelMixin:

    def post(self):
        json_data = request.get_json()
        serializer = self.get_serializer('post')
        validated_data = serializer.load(json_data)
        instance = self.perform_create(serializer, validated_data)
        return instance, HTTPStatus.CREATED

    def perform_create(self, serializer, validated_data):
        return serializer.create(validated_data)


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

    def put(self, id=None):
        json_data = request.get_json()
        serializer = self.get_serializer('put')
        validated_data = serializer.load(json_data)
        instance = self.get_instance(id)
        self.perform_update(instance, validated_data)
        return serializer.dump(instance), HTTPStatus.OK

    def perform_update(self, instance, validated_data):
        instance.update(validated_data)


class DeleteModelMixin:

    def delete(self, id=None):
        serializer = self.get_serializer('delete')
        instance = self.get_instance(id)
        self.perform_destroy(instance)
        return serializer.dump(instance), HTTPStatus.OK

    def perform_destroy(self, instance):
        instance.destroy()


class CRUDMixin(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DeleteModelMixin):
    pass
