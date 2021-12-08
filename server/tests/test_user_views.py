import pytest
import json
from http import HTTPStatus
from server.message_board import models
from server.extensions import db


@pytest.fixture
def test_user_data():
    return {
        'username': 'testuser',
        'email': 'email@test.com',
        'full_name': 'test test',
        'age': 1
    }


@pytest.fixture
def test_user(app, client, test_user_data):
    user = models.User(**test_user_data)
    with app.app_context():
        db.session.add(user)
        db.session.commit()


def remove_id_from_instance_dict(instance):
    return {k: v for k, v in instance.items() if k != 'id'}


def test_add_user(client, test_user_data):
    rv = client.post(
        'api/v1/users/',
        data=json.dumps(test_user_data),
        content_type='application/json'
    )
    assert rv.status_code == HTTPStatus.CREATED
    assert test_user_data == remove_id_from_instance_dict(rv.json)


def test_add_user_with_duplicated_email_fails(client, test_user, test_user_data):
    rv = client.post(
        'api/v1/users/',
        data=json.dumps(test_user_data),
        content_type='application/json'
    )
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json == {'_schema': ['Email is already taken']}


def test_add_user_with_unknown_fields(client, test_user_data):
    test_user_data['unknown_field'] = 'unknown_value'
    rv = client.post(
        'api/v1/users/',
        data=json.dumps(test_user_data),
        content_type='application/json'
    )
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json == {'unknown_field':  ['Unknown field.']}


def test_add_user_fails_if_email_is_not_valid(client, test_user_data):
    test_user_data['email'] = 'invalid_email'
    rv = client.post(
        'api/v1/users/',
        data=json.dumps(test_user_data),
        content_type='application/json'
    )
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json == {'email': ['Not a valid email address.']}


def test_retrieve_users(app, client, test_user_data):
    test_users = []
    with app.app_context():
        for index in range(5):
            current_test_user_data = test_user_data.copy()
            current_test_user_data['email'] = 'email%d@mail.com' % index
            user = models.User(**current_test_user_data)
            db.session.add(user)
            db.session.commit()
            test_users.append(user.to_dict)
    rv = client.get('api/v1/users/')
    assert rv.status_code == HTTPStatus.OK
    assert rv.json == test_users


def test_retrieve_user(app, client, test_user, test_user_data):
    user_id = 1
    rv = client.get(f'api/v1/users/{user_id}/')
    with app.app_context():
        user = models.User.query.filter_by(id=user_id).first()
    assert rv.status_code == HTTPStatus.OK
    assert user.to_dict == rv.json


def test_update_user(app, client, test_user):
    user_id = 1
    test_user_update_data = {'username': 'updated_test_user'}
    rv = client.put(
        f'api/v1/users/{user_id}/',
        data=json.dumps(test_user_update_data),
        content_type='application/json'
    )
    with app.app_context():
        user = models.User.query.filter_by(id=user_id).first()
    assert rv.status_code == HTTPStatus.OK
    assert rv.json == user.to_dict


def test_destroy_user(app, client, test_user):
    user_id = 1
    rv = client.delete(f'api/v1/users/{user_id}/')
    with app.app_context():
        user = models.User.query.filter_by(id=user_id).first()
    assert rv.status_code == HTTPStatus.OK
    assert not user
