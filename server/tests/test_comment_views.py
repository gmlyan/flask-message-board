from http import HTTPStatus
from server.message_board.models import Comment


def test_add_comment(app, client):
    test_comment_data = {'user_id': 2, 'post_id': 1, 'content': 'content3'}
    rv = client.post('api/v1/comments/', json=test_comment_data)
    assert rv.status_code == HTTPStatus.CREATED
    with app.app_context():
        assert Comment.query.count() == 3


def test_add_comment_with_nonexistent_user(client):
    test_comment_data = {'user_id': 100, 'post_id': 1, 'content': 'test_content'}
    rv = client.post('api/v1/comments/', json=test_comment_data)
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json == {'_schema': ['User does not exist']}


def test_add_comment_with_nonexistent_comment(client):
    test_comment_data = {'user_id': 2, 'post_id': 100, 'content': 'test_content'}
    rv = client.post('api/v1/comments/', json=test_comment_data)
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json == {'_schema': ['Post does not exist']}


def test_retrieve_comments(client):
    rv = client.get('api/v1/comments/')
    assert rv.status_code == HTTPStatus.OK
    assert len(rv.json) == 2


def test_retrieve_comment(client):
    rv = client.get('api/v1/comments/1/')
    assert rv.status_code == HTTPStatus.OK


def test_action_with_nonexistent_comment(client):
    rv = client.get('api/v1/comments/5/')
    assert rv.status_code == HTTPStatus.NOT_FOUND
    rv = client.put('api/v1/comments/5/', json={'content': 'new_content'})
    assert rv.status_code == HTTPStatus.NOT_FOUND
    rv = client.delete('api/v1/comments/5/')
    assert rv.status_code == HTTPStatus.NOT_FOUND


def test_update_comment(app, client):
    content = 'updated_content'
    rv = client.put('api/v1/comments/1/', json={'content': content})
    assert rv.status_code == HTTPStatus.OK
    with app.app_context():
        comment = Comment.query.filter_by(id=1).first()
        assert comment.content == content


def test_destroy_comment(app, client):
    rv = client.delete('api/v1/comments/1/')
    with app.app_context():
        comment = Comment.query.filter_by(id=1).first()
    assert rv.status_code == HTTPStatus.OK
    assert not comment


def test_destroy_comment_twice(client):
    client.delete('api/v1/comments/1/')
    rv = client.delete('api/v1/comments/1/')
    assert rv.status_code == HTTPStatus.NOT_FOUND
    assert rv.json == {'message': 'The requested URL was not found on the server. '
                                  'If you entered the URL manually please check your spelling and try again.'}
