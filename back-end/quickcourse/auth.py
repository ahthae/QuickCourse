from flask import Blueprint, current_app, jsonify, make_response, request, url_for
from flask_argon2 import Argon2
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies

from quickcourse.models import db, Student

jwt = JWTManager()
argon2 = Argon2()
bp = Blueprint('auth', __name__)

@bp.post('/login')
def login():
    username = request.json['username']
    password = request.json['password']

    student = db.session.scalar(db.select(Student).where(Student.username == username))
    if not student or not check_password(student.passhash, password):
        return jsonify({'message':'Invalid credentials.'}), 401

    response = jsonify({'message':'Login successful.'})
    access_token = create_access_token(identity=student)
    set_access_cookies(response, access_token)
    return response

@bp.post('/logout')
def logout():
    pass

@bp.post('/register')
def register():
    data = request.json

    student = Student(
        username=data['username'],
        passhash=hash_password(request.json['password']),
        name=data['name']
    )
    db.session.add(student)
    db.session.commit()

    return jsonify({
        'id': student.id,
        'name': student.name,
        'username': student.username,
        }), 201, { 'Location': url_for('student.student', id=student.id) }

@jwt.user_identity_loader
def jwt_identity_cb(student):
    return str(student.id)

@jwt.user_lookup_loader
def jwt_lookup_cb(jwt_header, jwt_data):
    id = int(jwt_data['sub'])
    return db.session.get(Student, id)

def pepper_password(password):
    return password+current_app.config['PEPPER']

def hash_password(password):
    return argon2.generate_password_hash(pepper_password(password))

def check_password(passhash, password):
    return argon2.check_password_hash(passhash, pepper_password(password))