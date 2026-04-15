import json
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.sqlite'

    if test_config is not None: app.config.from_mapping(test_config)
    else: app.config.from_file('config.json', load=json.load, silent=True)

    from quickcourse.models import db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from quickcourse import student, course
    app.register_blueprint(student.bp)
    app.register_blueprint(course.bp)

    return app
