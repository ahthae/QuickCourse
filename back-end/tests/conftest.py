import pytest
import tempfile

from quickcourse import create_app
from quickcourse.models import Course, db, Student

@pytest.fixture()
def app():
    tmp_fd, tmp_path = tempfile.mkstemp()

    app = create_app({
        'SECRET_KEY': 'secretkeysecretkeysecretkeysecretkey',
        'PEPPER': 'pepper',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{tmp_path}.sqlite',
        'SQLALCHEMY_RECORD_QUERIES': True,
        'TESTING': True,
        'JWT_TOKEN_LOCATION': ['cookies']
        })

    with app.app_context():
        course = Course(
            crn=1,
            name='Test 101',
            instructor='Test, Test',
            capacity=80
        )
        course2 = Course(
            crn=2,
            name='Test 202',
            instructor='Test2, Test2',
            capacity=35
        )
        student = Student(
            id=1,
            username='test',
            passhash='testtest',
            name='test test'
        )
        student.courses.append(course2)
        db.session.add(course)
        db.session.add(course2)
        db.session.add(student)

        db.session.commit()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()