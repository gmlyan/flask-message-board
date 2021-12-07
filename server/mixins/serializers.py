from server.extensions import db


class CreateMixin:

    def create(self, data):
        instance = self.Meta.model(**data)
        db.session.add(instance)
        db.session.commit()
        return self.dump(instance)
