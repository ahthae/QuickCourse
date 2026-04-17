from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from quickcourse.models import Course, db, Student, StudentCourseAssociation

admin = Admin(name="quickcourse")

admin.add_view(ModelView(Course, db.session, name="Course", endpoint='course_admin'))
admin.add_view(ModelView(Student, db.session, name="Student", endpoint='student_admin'))
