import pytest
from server import create_app
from server.extensions import db
from server.message_board import models


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def create_test_users(app):
    test_user_datas = [
        {'username': 'test_user1', 'email': 'email1@test.com', 'full_name': 'test', 'age': 1},
        {'username': 'test_user2', 'email': 'email2@test.com', 'full_name': 'test test', 'age': 2},
    ]
    with app.app_context():
        for user_data in test_user_datas:
            user = models.User(**user_data)
            db.session.add(user)
            db.session.commit()


@pytest.fixture(autouse=True)
def create_test_posts(app):
    test_post_datas = [
        {'user_id': 2, 'headline': 'headline1', 'content': 'content1'},
        {'user_id': 1, 'headline': 'headline2', 'content': 'content2'}
    ]
    with app.app_context():
        for post_data in test_post_datas:
            post = models.Post(**post_data)
            db.session.add(post)
            db.session.commit()


@pytest.fixture(autouse=True)
def create_test_comments(app):
    test_comment_datas = [
        {'user_id': 1, 'post_id': 2, 'content': 'content1'},
        {'user_id': 2, 'post_id': 1, 'content': 'content1'},
    ]
    with app.app_context():
        for comment_data in test_comment_datas:
            comment = models.Comment(**comment_data)
            db.session.add(comment)
            db.session.commit()
