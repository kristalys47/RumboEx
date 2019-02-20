from flask import jsonify, request, Blueprint
from flask_rbac import RBAC

# from RumboEx import rbac, Role, User
from RumboEx.handler.StudentHandler import StudentHandler



student_page = Blueprint('student_page', __name__)

from RumboEx.model.role import Role
from RumboEx.model.user import User

# failed attempt of creating rbac here
rbac = RBAC()
rbac.set_user_loader(lambda: current_user)
rbac.set_user_model(User)
rbac.set_role_model(Role)
#
# # Initial role for RBAC to work
start = Role('DUMMY')
rbacDummy = User(roles=[start])
#
# # To use this variable write global before the name in the methods
current_user = rbacDummy


# get a student by user id
@student_page.route('/student/<int:user_id>', methods=['GET'])
@rbac.allow(['student'], ['GET'], with_children=False)
def get_student(user_id):
    return StudentHandler().getStudent(user_id)

# get students of a mentor by mentor id
@student_page.route('/mentor/student/<int:user_id>', methods=['GET'])
def get_students(user_id):
    return StudentHandler().get_students_by_mentor_id(user_id)


@student_page.route('/student/course/tasks', methods=['GET'])
@rbac.exempt
# @rbac.allow(['counselor', 'psychologist'], ['GET'], with_children=False)
def get_students_by_mentor():
    return StudentHandler().get_students_with_courses_and_tasks()


@student_page.route('/student', methods=['POST', 'GET'])
@rbac.allow(['admin', 'counselor', 'advisor', 'mentor'], ['GET'], with_children=False)
def getallstudents():
    print(rbac)
    handler = StudentHandler()
    return handler.getallstudent()


@student_page.route('/users')
@rbac.allow(['admin'], ['GET'], with_children=False)
def getallusers():
    handler = StudentHandler()
    return handler.getallusers()
