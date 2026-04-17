import json
from flask import Blueprint, jsonify, make_response, request, url_for
from flask_jwt_extended import current_user, jwt_required

from quickcourse.models import Course, db, Student, StudentCourseAssociation

bp = Blueprint('course', __name__, url_prefix='/course')

@bp.route('/<int:crn>/register', methods=['POST'])
@jwt_required()
def register_current_user(crn):
    course = db.get_or_404(Course, crn, description=f'Course with CRN {crn} not found.')

    if len(course.students) >= course.capacity:
        return jsonify({'message': 'Failed to register: course at capacity.'}), 400

    if current_user not in course.students:
        course.students.append(current_user)
        db.session.commit()

    return jsonify({f'message':'Successfully registered for {crn}.'}), 200

@bp.route('/<int:crn>/withdraw', methods=['POST'])
@jwt_required()
def withdraw_current_user(crn):
    course = db.get_or_404(Course, crn, description=f'Course with CRN {crn} not found.')
    student = current_user

    if not student in course.students:
        return jsonify({'message': 'Failed to withdraw: not registered for course'}), 400

    try:
        course.students.remove(student)
        db.session.commit()
    except ValueError:
        return jsonify({'message': 'Student not enrolled in course'}), 400
    except:
        return jsonify({'message': 'Unable to withdraw from course.'}), 400
        
    return jsonify({f'message':'Successfully withdrawn from {crn}.'}), 200
    
@bp.route('/<int:crn>/register/<int:id>', methods=['GET', 'POST', 'PUT'])
@jwt_required()
def register(crn, id):
    course = db.get_or_404(Course, crn, description=f'Course with CRN {crn} not found.')
    student = db.get_or_404(Student, id, description=f'Student with ID {id} not found.')

    if (current_user.role == 0 and len(course.students) >= course.capacity):
        return jsonify({'message': 'Failed to register: course at capacity.'}), 400

    if student not in course.students:
        course.students.append(student)
        db.session.commit()

    return jsonify({f'message':'Successfully registered for {crn}.'}), 200

@bp.route('/<int:crn>/withdraw/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def withdraw(crn, id):
    course = db.get_or_404(Course, crn, description=f'Course with CRN {crn} not found.')
    student = db.get_or_404(Student, id, description=f'Student with ID {id} not found.')

    if current_user.role == 0 and not student in course.students:
        return jsonify({'message': 'Failed to withdraw: not registered for course'}), 400

    try:
        course.students.remove(student)
        db.session.commit()
    except ValueError:
        return jsonify({'message': 'Student not enrolled in course'}), 400
    except:
        return jsonify({'message': 'Unable to withdraw from course.'}), 400
        
    return jsonify({f'message':'Successfully withdrawn from {crn}.'}), 200

@bp.route('/<int:crn>/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def update_grade(crn, id):
    if (current_user.role == 0): return make_response(), 403
    
    association = db.get_or_404(StudentCourseAssociation, {'id': id, 'crn': crn}, description='Grade record for student {id} in course {crn} not found.')
    if association.course.instructor_id != current_user.id:
        return jsonify({'message': 'Only the instructor of this course may modify grades.'}), 400
    
    if (request.method == 'POST'):
        if not 'grade' in request.json: return make_response(), 400
        grade = request.json['grade']
        association.grade = grade
        db.session.commit()

    return jsonify({'grade': association.grade})

@bp.put('/')
@jwt_required()
def course_put():
    if current_user.role == 0:
        return jsonify({'message':'Unauthorized method.'}), 403

    data = request.get_json()

    try:
        course = Course(
            crn=data['crn'],
            name=data['name'],
            capacity=data['capacity']
        )
    except KeyError:
        return jsonify({'message':'Missing required data.'}), 400

    if 'instructor_id' in data:
        instructor = db.session.get(Student, data['instructor_id'])
        if not instructor:
            return jsonify({'message':f'Could not find instructor {data['instructor_id']}.'}), 400
        course.instructor = instructor
        course.instructor_id = instructor.id
            
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

@bp.get('/')
@jwt_required(optional=True)
def course_get_all():
    courses = db.session.scalars(db.select(Course)).all()
    data = [course.to_dict() for course in courses]
    if not current_user or current_user.role < 1:
        if 'students' in data: del data['students']
        if 'instructor' in data: del data['instructor_id']
    return jsonify(data)

@bp.route('/<int:crn>', methods=['GET', 'POST', 'DELETE'])
@jwt_required(optional=True)
def course(crn):
    if request.method != 'GET' and (not current_user or current_user.role < 1):
        return jsonify({'message': 'Unauthorized method'}), 403

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

    data = course.to_dict()
    if not current_user or current_user.role < 1:
        if 'students' in data: del data['students']
        if 'instructor' in data: del data['instructor_id']
    return data
