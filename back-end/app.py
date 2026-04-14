from typing import List 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.sqlite'
db = SQLAlchemy(app)

class StudentCourseAssociation(db.Model):
    student_id: Mapped[int] = mapped_column(ForeignKey('student.id'), primary_key=True)
    course_num: Mapped[int] = mapped_column(ForeignKey('course.num'), primary_key=True)
    student: Mapped[Student] = db.relationship(back_populates='course_associations')
    course: Mapped[Course] = db.relationship(back_populates='student_associations')
    grade: Mapped[float] = mapped_column(default=0)

class Student(db.Model):
    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    # TODO password
    course_associations: Mapped[List[StudentCourseAssociation]] = db.relationship(back_populates='student')
    courses: AssociationProxy[List[Course]] = association_proxy(
        'course_associations',
        'course',
        creator=lambda course_obj: StudentCourseAssociation(course=course_obj)
        )

class Course(db.Model):
    num: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    instructor: Mapped[str] = mapped_column()
    # TODO time
    capacity: Mapped[int] = mapped_column()
    student_associations: Mapped[List[StudentCourseAssociation]] = db.relationship(back_populates='course')
    students: AssociationProxy[List[Student]] = association_proxy(
        'student_associations', 
        'student',
        creator=lambda student_obj: StudentCourseAssociation(student=student_obj)
        )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Test record
        course = Course(
            num=101,
            name='Physics 101',
            instructor='Susan Walker',
            capacity=90
        )

        student = Student()
        student.id = 1
        student.name = 'Test Test'
        student.username = 'test'

        student.courses.append(course)
        
        db.session.add(student)
        db.session.commit()