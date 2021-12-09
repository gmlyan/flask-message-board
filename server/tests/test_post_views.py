from http import HTTPStatus
from server.message_board.models import Post


def test_add_post(app, client):
    test_post_data = {'user_id': 2, 'headline': 'headline3', 'content': 'content3'}
    rv = client.post('api/v1/posts/', json=test_post_data)
    assert rv.status_code == HTTPStatus.CREATED
    with app.app_context():
        assert Post.query.count() == 3


def test_add_post_with_nonexistent_user(client):
    test_post_data = {'user_id': 100, 'headline': 'headline100', 'content': 'content100'}
    rv = client.post('api/v1/posts/', json=test_post_data)
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json == {'_schema': ['User does not exist']}


def test_retrieve_posts(client):
    rv = client.get('api/v1/posts/')
    assert rv.status_code == HTTPStatus.OK
    assert len(rv.json) == 2


def test_retrieve_post(client):
    rv = client.get('api/v1/posts/1/')
    assert rv.status_code == HTTPStatus.OK


def test_action_with_nonexistent_post(client):
    rv = client.get('api/v1/posts/4/')
    assert rv.status_code == HTTPStatus.NOT_FOUND
    rv = client.put('api/v1/posts/4/', json={'headline': 'new_headline'})
    assert rv.status_code == HTTPStatus.NOT_FOUND
    rv = client.delete('api/v1/posts/4/')
    assert rv.status_code == HTTPStatus.NOT_FOUND


def test_update_post(app, client):
    headline = 'updated_hedline'
    rv = client.put('api/v1/posts/1/', json={'headline': headline})
    assert rv.status_code == HTTPStatus.OK
    with app.app_context():
        post = Post.query.filter_by(id=1).first()
        assert post.headline == headline


def test_destroy_post(app, client):
    rv = client.delete('api/v1/posts/1/')
    with app.app_context():
        post = Post.query.filter_by(id=1).first()
    assert rv.status_code == HTTPStatus.OK
    assert not post


def test_destroy_post_twice(client):
    client.delete('api/v1/posts/1/')
    rv = client.delete('api/v1/posts/1/')
    assert rv.status_code == HTTPStatus.NOT_FOUND
    assert rv.json == {'message': 'The requested URL was not found on the server. '
                                  'If you entered the URL manually please check your spelling and try again.'}
