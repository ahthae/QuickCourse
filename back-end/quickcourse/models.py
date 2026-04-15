from typing import List 

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy

db = SQLAlchemy()

class StudentCourseAssociation(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey('student.id'), primary_key=True)
    crn: Mapped[int] = mapped_column(ForeignKey('course.crn'), primary_key=True)
    student: Mapped[Student] = db.relationship(back_populates='course_associations')
    course: Mapped[Course] = db.relationship(back_populates='student_associations')
    grade: Mapped[float] = mapped_column(default=0)

class Student(db.Model):
    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    course_associations: Mapped[List[StudentCourseAssociation]] = db.relationship(
        back_populates='student',
        cascade='all, delete-orphan'
        )
    courses: AssociationProxy[List[Course]] = association_proxy(
        'course_associations',
        'course',
        creator=lambda course_obj: StudentCourseAssociation(course=course_obj)
        )

class Course(db.Model):
    crn: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str] = mapped_column()
    instructor: Mapped[str] = mapped_column()
    # TODO time
    capacity: Mapped[int] = mapped_column()
    student_associations: Mapped[List[StudentCourseAssociation]] = db.relationship(
        back_populates='course',
        cascade='all, delete-orphan'
        )
    students: AssociationProxy[List[Student]] = association_proxy(
        'student_associations', 
        'student',
        creator=lambda student_obj: StudentCourseAssociation(student=student_obj)
        )