import pytest
import tempfile

from quickcourse import create_app
from quickcourse.models import Course, db, Student
from quickcourse.auth import hash_password

@pytest.fixture()
def app():
    tmp_fd, tmp_path = tempfile.mkstemp()

    app = create_app({
        'SECRET_KEY': 'secretkeysecretkeysecretkeysecretkey',
        'PEPPER': 'pepper',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{tmp_path}.sqlite',
        'SQLALCHEMY_RECORD_QUERIES': True,
        'TESTING': True,
        'JWT_TOKEN_LOCATION': ['cookies'],
        'JWT_COOKIE_CSRF_PROTECT': False
        })

    with app.app_context():
        course = Course(
            crn=1,
            name='Test 101',
            capacity=80
        )
        course2 = Course(
            crn=2,
            name='Test 202',
            capacity=35
        )
        student = Student(
            id=1,
            username='test',
            passhash='testtest',
            name='test test'
        )
        teacher = Student(
            id=99,
            role=1,
            username='teach',
            passhash=hash_password('teachteach'),
            name='test teach'
        )
        student.courses.append(course2)
        course.instructor = teacher
        course.instructor_id = teacher.id
        course2.instructor = teacher 
        course2.instructor_id = teacher.id
        db.session.add(course)
        db.session.add(course2)
        db.session.add(student)
        db.session.add(teacher)

        db.session.commit()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()