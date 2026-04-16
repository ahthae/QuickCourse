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

    return jsonify({f'message':'Successfully registered for {crn}.'}), 200

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
        
    return jsonify({f'message':'Successfully withdrawn from {crn}.'}), 200

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
    return jsonify([course.to_dict() for course in courses])

@bp.put('/')
def course_put():
    data = request.get_json()

    try:
        course = Course(
            crn=data['crn'],
            name=data['name'],
            instructor=data['instructor'],
            capacity=data['capacity']
        )
    except KeyError:
        return jsonify({'message':'Missing required data.'}), 400

    if 'students' in data:
        for grade in data['students']:
            student = db.session.get(Student, grade['id'])
            if student is None:
                return jsonify({'message':f'Could not find student {grade['id']}.'}), 400
            else:
                course.student_associations.append(StudentCourseAssociation(
                    id=student.id,
                    crn=course.crn,
                    student=student,
                    course=course,
                    grade=grade['grade'] if 'grade' in grade else None
                ))

    db.session.add(course)
    db.session.commit()

    return jsonify(course.to_dict()), 201, { 'Location': url_for('course.course', crn=course.crn) }

@bp.route('/<int:crn>', methods=['GET', 'POST', 'DELETE'])
def course(crn):
    message_404 = f'Course with CRN {crn} not found.'
    course = db.get_or_404(Course, crn, description=message_404)

    if request.method == 'DELETE':
        db.session.delete(course)
        db.session.commit()
        return make_response(), 204

    if request.method == 'POST':
        data = request.json

        if 'crn' in data: course.crn = data['crn']
        if 'name' in data: course.name = data['name']
        if 'instructor' in data: course.instructor = data['instructor']
        if 'capacity' in data: course.capacity = data['capacity']

        db.session.commit()

    return course.to_dict()
