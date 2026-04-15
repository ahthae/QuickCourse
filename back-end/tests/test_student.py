import pytest
import json

from quickcourse.models import db

def test_student(client, app):
    data = {
            'username': "newtest",
            'password': "newtesttest",
            'name': "New Test"
          }
    response = client.put(f'/student/', json=data)
    assert response.status_code == 200

    id = response.json
    response = client.get(f'/student/{id}')

    assert response.status_code == 200
    assert response.json['id'] == id and \
           response.json['username'] == data['username'] and \
           response.json['name'] == data['name'] and \
           not response.json['courses']
    assert 'password' not in response.json

