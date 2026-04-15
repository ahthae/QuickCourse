import pytest
import json

from quickcourse.models import Course, Student, db

def test_course_get_all(client, app):
    pass

def test_course_get(client, app):
    crn = 1
    name='Test 101'
    instructor='Test, Test'
    capacity=80

    response = client.get(f'/course/{crn}')
    assert response.status_code == 200
    assert response.json['name'] == name
    assert response.json['instructor'] == instructor
    assert response.json['capacity'] == capacity

def test_course_update(client, app):
    crn = 1
    data = { 'name': 'updated' }

    response = client.post(f'/course/{crn}', json=data)
    assert response.status_code == 200
    assert response.json['name'] == 'updated'

def test_course_put(client, app):
    data = {
            'name': 'Create 101',
            'instructor': 'create, create',
            'capacity': 100 
          }
    response = client.put(f'/course/', json=data)
    assert response.status_code == 200

    with app.app_context():
        course = db.session.get_one(Course, response.json)
        assert course.name == data['name']
        assert course.instructor == data['instructor']
        assert course.capacity == data['capacity']

def test_course_delete(client, app):
    crn = 1

    response = client.delete(f'/course/{1}')

    assert response.status_code == 200
    assert response.json['crn'] == crn
    with app.app_context():
        assert db.session.get(Course, crn) == None
        assert db.session.get_one(Student, 1) != None