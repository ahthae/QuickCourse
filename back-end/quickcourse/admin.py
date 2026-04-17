from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from quickcourse.models import Course, db, Student, StudentCourseAssociation

admin = Admin(name="quickcourse")

class CourseView(ModelView):
    column_display_pk = True
    column_searchable_list = ['crn', 'name']
    column_editable_list = ['name', 'times', 'capacity']
    column_formatters = {
        'instructor': lambda v, c, m, n: m.instructor.name
    }

class StudentCourseView(ModelView):
    column_editable_list = ['grade']
    column_formatters = {
        'student': lambda v, c, m, n: m.student.name,
        'course': lambda v, c, m, n: m.course.name
    }
    column_formatters_detail = None

class StudentView(ModelView):
    column_searchable_list = ['id', 'name']
    column_editable_list = ['username', 'name', 'role']
    column_exclude_list = ['passhash']
    column_display_pk = True

admin.add_view(CourseView(Course, db.session, name="Course", endpoint='course_admin'))
admin.add_view(StudentView(Student, db.session, name="Student", endpoint='student_admin'))
admin.add_view(StudentCourseView(StudentCourseAssociation, db.session, name="Grades", endpoint='grades_admin'))
