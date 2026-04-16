from flask import Blueprint, current_app, jsonify, make_response, redirect, request, url_for

from quickcourse.models import Course, db, Student, StudentCourseAssociation
from quickcourse.auth import hash_password

bp = Blueprint('student', __name__, url_prefix='/student')

@bp.get('/')
def student_get_all():
    students = db.session.scalars(db.select(Student)).all()
    return jsonify([student.to_dict() for student in students])

@bp.put('/')
def student_put():
    data = request.get_json()

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

    return student.to_dict()