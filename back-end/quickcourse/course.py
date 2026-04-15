import json
from flask import Blueprint, jsonify, request

from quickcourse.models import db, Course

bp = Blueprint('course', __name__, url_prefix='/course')

@bp.route('/<int:crn>/<int:id>')
def register(crn, id):
    pass

@bp.route('/<int:crn>/<int:id>')
def withdraw(crn, id):
    pass

@bp.put('/')
def course_put():
    data = request.get_json()

    course = Course(
        name=data['name'],
        instructor=data['instructor'],
        capacity=data['capacity']
    )

    db.session.add(course)
    db.session.commit()

    return jsonify(course.crn)

@bp.route('/<int:crn>', methods=['GET', 'POST', 'DELETE'])
def course(crn):
    message_404 = f'Course with CRN {crn} not found.'
    course = db.get_or_404(Course, crn, description=message_404)

    # save students before possibly deleting the associations
    students = [{'id': a.student.id, 'grade': a.grade} for a in course.student_associations]

    if request.method == 'DELETE':
        db.session.delete(course)
        db.session.commit()
    elif request.method == 'POST':
        data = request.json

        if 'crn' in data: course.crn = data['crn']
        if 'name' in data: course.name = data['name']
        if 'instructor' in data: course.instructor = data['instructor']
        if 'capacity' in data: course.capacity = data['capacity']

        db.session.commit()

        # TODO update student list maybe?
        # could be better to enforce validation by making client use register/withdraw enpoints
        # note: PUT also doesn't handle students

    return {
        'crn': course.crn,
        'name': course.name,
        'instructor': course.instructor,
        'capacity': course.capacity,
        'students': students
    }

@bp.route('/<int:crn>/<int:id>/<float:grade>')
def update_grade(crn, id, grade):
    pass
