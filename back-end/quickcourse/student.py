from flask import Blueprint, current_app, jsonify, request, url_for

from quickcourse.models import db, Student

bp = Blueprint('student', __name__, url_prefix='/student')

@bp.get('/')
def student_get():
    students = db.session.scalars(db.select(Student)).all()

    return jsonify([{
        'id': student.id,
        'name': student.name,
        'username': student.username,
        'passhash': student.passhash,
        'courses': [{'crn': a.course.crn, 'id': a.grade} for a in student.courses]
    } for student in students])

@bp.put('/')
def student_put():
    data = request.get_json()

    student = Student(
        username=data['username'],
        passhash=data['passhash'],
        name=data['name'],
    )

    db.session.add(student)
    db.session.commit()

    response = jsonify(student.id)
    return response, 200, { 'Location': url_for('student.student', id=student.id) }

@bp.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
def student(id):
    student = db.get_or_404(Student, id, description=f'Student with ID {id} not found.')

    courses = [{'crn': a.course.crn, 'grade': a.grade} for a in student.course_associations]

    if (request.method == 'DELETE'):
        db.session.delete(student)
        db.session.commit()
    elif (request.method == 'POST'):
        data = request.json
        if 'id' in data: student.id = data['id']
        if 'name' in data: student.name = data['name']
        if 'username' in data: student.username = data['username']
        if 'passhash' in data: student.password = data['passhash'] # TODO
        db.session.commit()

    return {
        'id': student.id,
        'username': student.username,
        'name': student.name,
        'courses': courses
    }