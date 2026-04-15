import json
from flask import Blueprint, jsonify, make_response, request, url_for

from quickcourse.models import Course, db, Student, StudentCourseAssociation

bp = Blueprint('course', __name__, url_prefix='/course')

@bp.route('/<int:crn>/register/<int:id>', methods=['GET', 'POST', 'PUT'])
def register(crn, id):
    course = db.get_or_404(Course, crn, description=f'Course with CRN {crn} not found.')
    student = db.get_or_404(Student, id, description=f'Student with ID {id} not found.')

    course.students.append(student)
    db.session.commit()

    return make_response(), 204

@bp.route('/<int:crn>/withdraw/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def withdraw(crn, id):
    course = db.get_or_404(Course, crn, description=f'Course with CRN {crn} not found.')
    student = db.get_or_404(Student, id, description=f'Student with ID {id} not found.')

    try:
        course.students.remove(student)
        db.session.commit()
    except ValueError:
        return jsonify({'message': 'Student not enrolled in course'}), 400
    except:
        return jsonify({'message': 'Unable to withdraw from course.'}), 400
        
    return make_response(), 204

@bp.route('/<int:crn>/<int:id>', methods=['GET', 'POST'])
def update_grade(crn, id):
    association = db.get_or_404(StudentCourseAssociation, {'id': id, 'crn': crn}, description='Grade record for student {id} in course {crn} not found.')
    
    if (request.method == 'POST'):
        if not 'grade' in request.json: return make_response(), 400
        grade = request.json['grade']
        association.grade = grade
        db.session.commit()

    return jsonify({'grade': association.grade})

@bp.get('/')
def course_get():
    courses = db.session.scalars(db.select(Course)).all()
    return jsonify([{
        'crn': course.crn,
        'name': course.name,
        'instructor': course.instructor,
        'capacity': course.capacity,
        'students': [{'id': a.student.id, 'grade': a.grade} for a in course.student_associations]
    } for course in courses]), 200

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

    response = jsonify(course.crn)
    return response, 200, { 'Location': url_for('course.course', crn=course.crn) }

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
