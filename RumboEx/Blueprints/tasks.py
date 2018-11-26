from flask import Blueprint, request, jsonify
from RumboEx import rbac
from RumboEx.handler.taskHandler import TaskHandler


tasks = Blueprint('tasks', __name__)


# get personal tasks by user id
@tasks.route('/task/personal/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@rbac.allow(['student'], ['OPTIONS', 'POST', 'GET'], with_children=False)
def get_personal_tasks(student_id):
    print(request)
    global current_user
    if request.method == 'GET':
        return TaskHandler().get_personal_task_by_user_id(student_id)
    # why do i have to put options instead of post
    elif request.method == 'OPTIONS':
        print('request', request, request.data, request.form, request.get_json())
        return TaskHandler().insert_personal_task(student_id, request.data)


# get study tasks by user id
@tasks.route('/task/study/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@rbac.allow(['student'], ['OPTIONS', 'POST', 'GET'], with_children=False)
def get_study_tasks(student_id):
    if request.method == 'GET':
        return TaskHandler().get_study_task_by_user_id(student_id)
    elif request.method == 'OPTIONS':
        print('json:', request.get_json())
        print('request:', request)
        print('data:', request.data)
        return TaskHandler().insert_study_task(student_id, request.get_json())


# get course tasks by user id
@tasks.route('/task/course/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@rbac.allow(['student'], ['OPTIONS', 'POST', 'GET'], with_children=False)
def get_course_tasks(student_id):
    return TaskHandler().get_course_task_by_user_id(student_id)


# get appointment tasks by user id
@tasks.route('/task/appointment/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@rbac.allow(['student'], ['OPTIONS', 'POST', 'GET'], with_children=False)
def get_appointment_tasks(student_id):
    return TaskHandler().get_appointment_tasks_by_user_id(student_id)


# get study tasks of a specific course by user id and course id
@tasks.route('/task/study/<int:student_id>/<int:course_id>', methods=['GET'])
@rbac.allow(['student'], ['GET'], with_children=False)
def get_study_tasks_by_course_id(student_id, course_id):
    return TaskHandler().get_study_task_by_user_id_and_course_id(student_id, course_id)


# get all tasks; for testing purposes
@tasks.route('/task', methods=['GET'])
@rbac.exempt
def get_all_tasks():
    return TaskHandler().get_all_tasks()
