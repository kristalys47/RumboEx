from flask import jsonify, request, Blueprint
from RumboEx.decorators.authorization import authorize
from flask_cors import CORS
from flask_rbac import RBAC

# from RumboEx import rbac, Role, User
from RumboEx.handler.StudentHandler import StudentHandler



student_page = Blueprint('student_page', __name__)
CORS(student_page)

# get a student by user id
@student_page.route('/student/<int:user_id>', methods=['GET', 'OPTIONS', 'PUT'])
@authorize(['student'])
def get_student(user_id):
    if request.method == 'GET':
        return StudentHandler().getStudent(user_id)
    elif request.method == 'PUT':
        cred = request.get_json()
        if 'phone_num' in cred:
            return StudentHandler().changePhoneNum(user_id, cred['phone_num'])
        if 'student_num' in cred:
            return StudentHandler().changeStudentNum(user_id, cred['student_num'])
        if 'program' in cred:
            return StudentHandler().changeProgram(user_id, cred['program'])
        if 'name' in cred:
            return StudentHandler().changeName(user_id, cred['name'])
        if 'lastname' in cred:
            return StudentHandler().changeLastname(user_id, cred['lastname'])
        if 'username' in cred:
            return StudentHandler().changeUsername(user_id, cred['username'])
        if 'email' in cred:
            return StudentHandler().changeEmail(user_id, cred['email'])
        if 'password' in cred:
            return StudentHandler().changePassword(user_id, cred['password'])

# get students of a mentor by mentor id
@student_page.route('/studentlist/<int:user_id>', methods=['GET'])
def get_students(user_id):
    return StudentHandler().get_students_by_mentor_id(user_id)


@student_page.route('/student/course/tasks', methods=['GET'])
# @rbac.allow(['counselor', 'psychologist'], ['GET'], with_children=False)
def get_students_by_mentor():
    return StudentHandler().get_students_with_courses_and_tasks()


@student_page.route('/studentlist', methods=['POST', 'GET'])
@rbac.allow(['admin', 'counselor', 'advisor', 'mentor'], ['GET'], with_children=False)
def getallstudents():
    print(rbac)
    handler = StudentHandler()
    return handler.get_students_with_courses_and_tasks()

# @student_page.route('/studentlist/<int:mentorid>', methods=['POST', 'GET'])
# @rbac.allow(['admin', 'counselor', 'advisor', 'mentor'], ['GET'], with_children=False)
# def get_students_by_mentor_id():
#     print(rbac)
#     handler = StudentHandler()
#     return handler.get_students_with_courses_and_tasks()


@student_page.route('/users')
@rbac.allow(['admin'], ['GET'], with_children=False)
def getallusers():
    handler = StudentHandler()
    return handler.getallusers()
