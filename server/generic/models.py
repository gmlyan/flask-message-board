from server.extensions import db


class Model(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.id)
