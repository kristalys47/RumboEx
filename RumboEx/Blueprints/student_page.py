from flask import jsonify, request, Blueprint
from RumboEx import rbac
from RumboEx.handler.StudentHandler import StudentHandler


student_page = Blueprint('student_page', __name__)


@student_page.route('/student/<int:user_id>', methods=['GET'])
@rbac.allow(['student'], ['GET'], with_children=False)
def get_student(user_id):
    print(StudentHandler().getStudent(user_id))
    return StudentHandler().getStudent(user_id)


@student_page.route('/student/course/tasks', methods=['GET'])
@rbac.exempt
# @rbac.allow(['counselor', 'psychologist'], ['GET'], with_children=False)
def get_students():
    return StudentHandler().get_students_with_courses_and_tasks()


@student_page.route('/student', methods=['POST', 'GET'])
@rbac.allow(['admin', 'counselor', 'advisor', 'mentor'], ['GET'], with_children=False)
def getallstudents():
    handler = StudentHandler()
    return handler.getallstudent()


@student_page.route('/users')
@rbac.allow(['admin'], ['GET'], with_children=False)
def getallusers():
    handler = StudentHandler()
    return handler.getallusers()
