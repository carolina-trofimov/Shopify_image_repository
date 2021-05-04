import pytest
from server import app as flask_app
from model import db, connect_to_db

@pytest.fixture(scope='function')
def app():
    yield flask_app

@pytest.fixture(scope='function')
def client(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['TESTING'] = True
    
    connect_to_db(app)
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()