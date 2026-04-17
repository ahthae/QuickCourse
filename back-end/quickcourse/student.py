from flask import Blueprint, current_app, jsonify, make_response, redirect, request, url_for
from flask_jwt_extended import current_user, jwt_required

from quickcourse.models import Course, db, Student, StudentCourseAssociation
from quickcourse.auth import hash_password

bp = Blueprint('student', __name__, url_prefix='/student')

@bp.get('/')
@jwt_required()
def student_get_all():
    if current_user.role == 0:
        return make_response(), 403
    students = db.session.scalars(db.select(Student)).all()
    return jsonify([student.to_dict() for student in students])

@bp.put('/')
@jwt_required()
def student_put():
    data = request.get_json()

    if current_user.role == 0:
        return jsonify({'message':'Unauthorized method.'}), 403

    try:
        student = Student(
            id=data['id'],
            username=data['username'],
            passhash=hash_password(data['password']),
            name=data['name']
        )
    except KeyError:
        return jsonify({'message':'Missing required data.'}), 400

    if 'courses' in data:
        for grade in data['courses']:
            course = db.session.get(Course, grade['crn'])
            if course is None:
                return jsonify({'message':f'Could not find course {grade['crn']}.'}), 400
            else:
                student.course_associations.append(StudentCourseAssociation(
                    id=student.id,
                    crn=course.crn,
                    student=student,
                    course=course,
                    grade=grade['grade'] if 'grade' in grade else None
                ))

    db.session.add(student)
    db.session.commit()

    return jsonify(student.to_dict()), 201, { 'Location': url_for('student.student', id=student.id) }

@bp.route('/<string:username>', methods=['GET', 'POST', 'DELETE'])
def student_username(username):
    id = db.one_or_404(db.select(Student.id).where(Student.username == username))
    return redirect(url_for('student.student', id=id))

@bp.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
@jwt_required(optional=True)
def student(id):
    student = db.get_or_404(Student, id, description=f'Student with ID {id} not found.')

    if (request.method == 'DELETE'):
        db.session.delete(student)
        db.session.commit()
        return make_response(), 204
        

    if (request.method == 'POST'):
        data = request.json
        if 'id' in data: student.id = data['id']
        if 'name' in data: student.name = data['name']
        if 'username' in data: student.username = data['username']
        if 'password' in data: student.passhash = hash_password(data['password'])
        db.session.commit()

    data = student.to_dict()

    if current_user and current_user.role == 0 and current_user.id != id:
        del data['courses']

    return data