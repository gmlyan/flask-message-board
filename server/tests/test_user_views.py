from http import HTTPStatus
from server.message_board.models import User


def test_add_user(app, client):
    test_user_data = {'username': 'new_test_user', 'email': 'test_email@test.com', 'full_name': 'test test', 'age': 1}
    rv = client.post('api/v1/users/', json=test_user_data)
    assert rv.status_code == HTTPStatus.CREATED
    with app.app_context():
        assert User.query.count() == 3


def test_add_user_fails_if_email_is_not_valid(client):
    rv = client.post('api/v1/users/', json={'username': 'test_user', 'email': 'invalid_email'})
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json == {'email': ['Not a valid email address.']}


def test_add_user_with_duplicated_email_fails(client):
    test_user_data = {'username': 'test_user', 'email': 'email1@test.com'}
    rv = client.post('api/v1/users/', json=test_user_data)
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json == {'_schema': ['Email is already taken']}


def test_retrieve_users(client):
    rv = client.get('api/v1/users/')
    assert rv.status_code == HTTPStatus.OK
    assert len(rv.json) == 2


def test_retrieve_user(client):
    rv = client.get('api/v1/users/1/')
    assert rv.status_code == HTTPStatus.OK


def test_action_with_nonexistent_user(client):
    rv = client.get('api/v1/users/6/')
    assert rv.status_code == HTTPStatus.NOT_FOUND
    rv = client.put('api/v1/users/6/', json={'username': 'test_user'})
    assert rv.status_code == HTTPStatus.NOT_FOUND
    rv = client.delete('api/v1/users/6/')
    assert rv.status_code == HTTPStatus.NOT_FOUND


def test_update_user(app, client):
    username = 'updated_test_user'
    rv = client.put('api/v1/users/1/', json={'username': username})
    assert rv.status_code == HTTPStatus.OK
    with app.app_context():
        user = User.query.filter_by(id=1).first()
        assert user.username == username


def test_destroy_user(app, client):
    rv = client.delete('api/v1/users/1/')
    with app.app_context():
        user = User.query.filter_by(id=1).first()
    assert rv.status_code == HTTPStatus.OK
    assert not user


def test_destroy_user_twice(client):
    client.delete('api/v1/users/1/')
    rv = client.delete('api/v1/users/1/')
    assert rv.status_code == HTTPStatus.NOT_FOUND
    assert rv.json == {'message': 'The requested URL was not found on the server. '
                                  'If you entered the URL manually please check your spelling and try again.'}
