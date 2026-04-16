from quickcourse.models import db, Student
from quickcourse.auth import argon2, hash_password

def test_register(client, app):
    data = {
        'username': 'thisisausername',
        'password': 'thisisapassword',
        'name': 'Reggie Ster'
    }

    response = client.post('/register', json=data)
    assert response.status_code == 201

    assert response.json['username'] == data['username']
    assert response.json['name'] == data['name']
    assert 'id' in response.json
    assert 'password' not in response.json
    assert 'passhash' not in response.json

    with app.app_context():
        student = db.session.get(Student, response.json['id'])
        assert student is not None
        assert student.passhash != ''
        assert student.passhash != data['password'] # Make sure we hashed the password
 
    # Make sure the hashed password is peppered
    assert not argon2.check_password_hash(student.passhash, data['password'])
    assert argon2.check_password_hash(student.passhash, data['password']+app.config['PEPPER'])

def test_login(client, app):
    bad_data = {
        'username': 'incorrect username',
        'password': 'incorrect password',
        'name': 'Reggie Ster'
    }
    data = {
        'username': 'test',
        'password': 'testtest',
        'name': 'test test'
    }
    with app.app_context():
        passhash = hash_password(data['password'])
        db.session.get_one(Student, 1).passhash = passhash
        db.session.commit()

    response = client.post('/login', json=bad_data)
    assert response.status_code == 401
    assert client.get_cookie('access_token_cookie') is None

    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert client.get_cookie('access_token_cookie') is not None
