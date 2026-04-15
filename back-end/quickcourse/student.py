from flask import Blueprint, current_app, jsonify, request

from quickcourse.models import db, Student

bp = Blueprint('student', __name__, url_prefix='/student')

@bp.put('/')
def student_put():
    data = request.get_json()

    student = Student(
        username=data['username'],
        password=data['password'],
        name=data['name'],
    )

    db.session.add(student)
    db.session.commit()

    return jsonify(student.id)

@bp.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
def student(id):
    if request.method == 'GET':
        student = db.get_or_404(Student, id, description=f'Student with ID {id} not found.')

        return {
            'id': student.id,
            'username': student.username,
            'name': student.name,
            'courses': [{'crn': a.course.crn, 'grade': a.grade} for a in student.course_associations]
        }