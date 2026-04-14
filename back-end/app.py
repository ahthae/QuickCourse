from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Student, Course

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.sqlite'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():

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