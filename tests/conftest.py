import pytest
from app import create_app, db


@pytest.fixture(scope='function')
def test_app():
    """Fixture to create a Flask app for testing."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    # Push an application context for testing
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def test_client(test_app):
    """Provides a test client for the app."""
    return test_app.test_client()


@pytest.fixture(scope='function')
def test_db(test_app):
    """Provides a transactional scope around tests."""
    with test_app.app_context():
        yield db
