from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from RumboEx import rbac
from RumboEx.handler.CourseHandler import CourseHandler


courses = Blueprint('courses', __name__)
CORS(courses)

# get courses a student is enrolled in by user id
@courses.route('/course/<int:student_id>', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin()
@rbac.allow(['student'], ['GET', 'POST', 'OPTIONS'], with_children=False)
def get_student_courses(student_id):
    print(request)
    print(request.get_json())
    if request.method == 'GET':
        return CourseHandler().get_course(student_id)
    # elif request.method == 'OPTIONS':
    #     return
    elif request.method == 'POST':
        print(request.get_json())
        return CourseHandler().insert_course(student_id, request.get_json())

@courses.route('/course/<int:course_id>/<int:student_id>', methods=['GET'])
@cross_origin()
def get_course(course_id,student_id):
    if request.method == 'GET':
        return CourseHandler().get_course_by_course_id(course_id, student_id)


# get courses a student is enrolled in with grades by user id
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

@courses.route('/grade/<int:student_id>', methods=['OPTIONS', 'POST', 'PUT'])
@cross_origin()
def insert_grade(student_id):
    if request.method == 'POST':
        return CourseHandler().insert_grade(student_id, request.get_json())
    elif request.method == 'PUT':
        cred = request.get_json()
        grade_id = cred['g_id']
        if 'g_name' in cred:
            return CourseHandler().changeGradeName(grade_id, cred['g_name'])
        if 'grade' in cred:
            return CourseHandler().changeGradeGrade(grade_id, cred['grade'])
        if 'weight' in cred:
            return CourseHandler().changeGradeWeight(grade_id, cred['weight'])
        if 'total' in cred:
            return CourseHandler().changeGradeTotal(grade_id, cred['total'])
        if 'date' in cred:
            return CourseHandler().changeGradeDate(grade_id, cred['date'])

@courses.route('/grade/<int:student_id>/<int:grade_id>', methods=['DELETE'])
@cross_origin()
def delete_grade(student_id, grade_id):
    if request.method == 'DELETE':
        return CourseHandler().deleteGrade(student_id, grade_id)
