import pytest
import json

from quickcourse.models import Course, db, Student

def test_student_get_all(client, app):
    student = Student(
        username='newtest',
        passhash='newtesttest',
        name='New Test'
    )
    with app.app_context():
        db.session.add(student)
        db.session.commit()
    
    response = client.get('/student/')
    assert response.status_code == 200
 
    students = response.json
    assert len(students) == 2

def test_student_get(client, app):
    id = 1
    username='test'
    passhash='testtest'
    name='test test'
 
    response = client.get(f'/student/{id}')
    assert response.status_code == 200
 
    assert response.json['id'] == id
    assert response.json['username'] == username
    assert response.json['name'] == name
    assert 'passhash' not in response.json

def test_student_put(client, app):
    data = {
        'username':'newtest',
        'passhash':'newtesttest',
        'name':'New Test'
    }
    response = client.put(f'/student/', json=data)
    assert response.status_code == 200

    with app.app_context():
        student = db.session.get(Student, response.json)
        assert student is not None
        assert student.username == data['username']
        assert student.name == data['name']
        assert student.passhash == data['passhash']

def test_student_update(client, app):
    id = 1
    data = { 'username': 'updated' }

    response = client.post(f'/student/{id}', json=data)
    assert response.status_code == 200
    assert response.json['username'] == 'updated'

def test_course_delete(client, app):
    id = 1

    response = client.delete(f'/student/{id}')

    assert response.status_code == 200
    assert response.json['id'] == id
    with app.app_context():
        assert db.session.get(Student, id) is None
        assert db.session.get_one(Course, 1) is not None