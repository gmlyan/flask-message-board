from http import HTTPStatus
from flask import abort
from sqlalchemy.orm import exc


def get_object_or_404(fn, *args, **kwargs):
    try:
        rv = fn(*args, **kwargs)
        if rv is None:
            abort(HTTPStatus.NOT_FOUND)
        return rv
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(HTTPStatus.NOT_FOUND)
