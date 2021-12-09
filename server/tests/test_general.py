from http import HTTPStatus


def test_ping(client):
    rv = client.get('api/v1/ping/')
    assert rv.status_code == HTTPStatus.OK
    assert rv.json == {'Ping': 'Pong'}


def test_resource_which_not_exist(client):
    rv = client.get('invalid_endpoint/')
    assert rv.status_code == HTTPStatus.NOT_FOUND
