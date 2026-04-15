import pytest
import json
from flask import jsonify
from quickcourse.models import db, Student, Course

def test_student(client, app):
    data = {
            'id': 8,
            'username': "test",
            'password': "testtest",
            'name': "test test"
          }
    response = client.put(f'/student/', json=data)
    assert response.status_code == 200

    id = response.json
    response = client.get(f'/student/{id}')

    assert response.status_code == 200
    assert response.json['id'] == id and \
           response.json['username'] == 'test' and \
           response.json['name'] == 'test test' and \
           not response.json['courses']
    assert 'password' not in response.json

