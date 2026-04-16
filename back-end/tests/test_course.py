import pytest
import json

from quickcourse.models import Course, Student, db

def test_register(client, app):
    crn = 1
    id = 1

    assert client.get(f'/course/{crn}/register/{id}').status_code == 200

    with app.app_context():
        course = db.session.get_one(Course, 1)
        student = db.session.get_one(Student, 1)
        assert len(course.students) == 1
        assert len(student.courses) == 2
        assert course.students[0].id == student.id
        assert student.courses[0].crn == course.crn

def test_withdraw(client, app):
    crn = 1
    id = 1

    # Withdraw from a course we're not registered for
    assert client.get(f'/course/{crn}/withdraw/{id}').status_code == 400

    # Withdraw from a course we are register for
    assert client.get(f'/course/{crn}/register/{id}').status_code == 200
    assert client.get(f'/course/{crn}/withdraw/{id}').status_code == 200

    with app.app_context():
        course = db.session.get_one(Course, 1)
        student = db.session.get_one(Student, 1)
        assert course is not None
        assert student is not None
        assert len(course.students) == 0
        assert len(student.courses) == 1

def test_update_grade(client, app):
    grade = 98
    crn = 2
    id = 1

    response = client.get(f'/course/{crn}/{id}')
    assert response.status_code == 200
    assert response.json['grade'] == 0

    response = client.post(f'/course/{crn}/{id}', json={'grade':grade})
    assert response.status_code == 200
    assert response.json['grade'] == grade

def test_course_get_all(client, app):
    response = client.get('/course/')

    assert response.status_code == 200
    assert len(response.json) == 2

def test_course_get(client, app):
    crn = 2
    name='Test 202'
    instructor='Test2, Test2'
    capacity=35

    response = client.get(f'/course/{crn}')
    assert response.status_code == 200
    assert response.json['name'] == name
    assert response.json['instructor'] == instructor
    assert response.json['capacity'] == capacity
    assert len(response.json['students']) == 1
    assert response.json['students'][0]['id'] == 1

def test_course_update(client, app):
    crn = 1
    data = { 'name': 'updated' }

    response = client.post(f'/course/{crn}', json=data)
    assert response.status_code == 200
    assert response.json['name'] == 'updated'

def test_course_put(client, app):
    data = {
            'crn': 3,
            'name': 'Create 101',
            'instructor': 'create, create',
            'capacity': 100 ,
            'students': [{'id': 1}]
          }
    response = client.put(f'/course/', json=data)
    assert response.status_code == 201

    with app.app_context():
        course = db.session.get_one(Course, response.json['crn'])
        assert course.name == data['name']
        assert course.instructor == data['instructor']
        assert course.capacity == data['capacity']
        assert len(course.students) == 1
        assert course.students[0].id == 1

def test_course_delete(client, app):
    crn = 2

    assert client.delete(f'/course/{crn}').status_code == 204

    with app.app_context():
        assert db.session.get(Course, crn) is None
        student = db.session.get_one(Student, 1)
        assert student is not None
        assert len(student.courses) == 0