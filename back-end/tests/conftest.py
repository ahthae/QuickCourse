import pytest
import tempfile

from quickcourse import create_app

@pytest.fixture()
def app():
    tmp_fd, tmp_path = tempfile.mkstemp()

    app = create_app({
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{tmp_path}.sqlite',
        'TESTING': True
        })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()