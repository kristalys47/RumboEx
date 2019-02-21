from flask import Blueprint, request
from RumboEx import rbac
from RumboEx.handler.CourseHandler import CourseHandler


courses = Blueprint('courses', __name__)


# get courses a student is enrolled in by user id
@courses.route('/course/<int:student_id>', methods=['GET', 'OPTIONS', 'POST'])
@rbac.allow(['student'], ['GET'], with_children=False)
def get_student_courses(student_id):
    if request.method == 'GET':
        return CourseHandler().get_courses_by_student_id(student_id)
    elif request.method == 'POST':
        return CourseHandler().insert_course(student_id, request.get_json())


# get courses a student is enrolled in with grades bu user id
@courses.route('/courses/<int:student_id>', methods=['GET'])
@rbac.allow(['student'], ['GET'], with_children=False)
def get_student_courses_with_grades(student_id):
    return CourseHandler().get_courses_with_grades_by_student_id(student_id)

# get a course by course id
# @courses.route('/course/<int:course_id>', methods=['GET'])
# @rbac.allow(['student'], ['GET'], with_children=False)
# def get_course(course_id):
#     return CourseHandler().get_course_by_course_id(course_id)


# get grades of a course by course id
@courses.route('/course/<int:course_id>/grades', methods=['GET'])
@rbac.allow(['student'], ['GET'], with_children=False)
def get_grades_by_course_id(course_id):
    print(course_id)
    return CourseHandler().get_grades_by_course_id(course_id)

@courses.route('/grade/<int:student_id>', methods=['OPTIONS', 'POST'])
def insert_grade(student_id):
    return CourseHandler().insert_grade(student_id, request.get_json())
