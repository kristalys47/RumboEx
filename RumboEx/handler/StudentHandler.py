from RumboEx.dao.StudentDAO import StudentDAO
from RumboEx.dao.CourseDao import CourseDAO
from RumboEx.dao.taskDao import TaskDAO
from RumboEx.handler.CourseHandler import CourseHandler
from RumboEx.handler.taskHandler import TaskHandler
from flask import jsonify
from RumboEx.handler.emails import EmailHandler


class StudentHandler:

    def dicUser(self, user):
        return {'user_id': user[0], 'username': user[1], 'name': user[2], 'lastname': user[3]}

    def dicStudent(self, student):
        print(student)
        return {
            'user_id': student[0],
            'username': student[1],
            'name': student[2],
            'lastname': student[3],
            'email': student[4],
            'password': student[5],
            'student_num': student[6],
            'program_num': student[7],
            'program_name': student[8],
            'faculty_num': student[9],
            'faculty_name': student[10],
            'role_num': student[11],
            'role_name': student[12],
            'phone_num': student[13]
        }

    # why we have this double??
    def dicUser(self, user):
        return {'user_id': user[0], 'username': user[1], 'name': user[2], 'lastname': user[3]}

    def insertStudent(self, username, email, password, name, lastname, program, student_num, phone_num):
        calltoInsert = StudentDAO().insertStudent(username, email, password, name, lastname, program, student_num, phone_num)
        # todo: fix this method
        # EmailHandler().send_mail_after_register(calltoInsert)
        return jsonify(result=calltoInsert), 200

    def getallusers(self):
        users = StudentDAO().getallusers()
        result = []
        for user in users:
            result.append(self.dicUser(user))
        return jsonify(Users=result), 200

    def getallstudent(self):
        students = StudentDAO().getallstudent()
        if not students:
            return jsonify(Error='NOT FOUND'), 404
        result = []
        for student in students:
            result.append(self.dicStudent(student))
        return jsonify(Users=result), 200

    def get_students_with_courses_and_tasks(self):
        dao = StudentDAO()
        students = dao.getallstudent()
        if not students:
            return jsonify(Error='NOT FOUND'), 404
        mapped_result = []
        for s in students:
            student = self.dicStudent(s)
            courses = CourseHandler().get_courses_with_grades_by_student_id(student['user_id'])
            print(courses)
            if courses[1] is 200:
                student['courses'] = courses[0].get_json()
            tasks = TaskHandler().get_all_tasks_by_user_id(student['user_id'])
            if tasks[1] is 200:
                student['tasks'] = tasks[0].get_json()
            # student['tasks'] = TaskDAO().get
            mapped_result.append(student)
        return jsonify(mapped_result), 200

    def get_students_by_mentor_id(self, mentor_id):
        dao = StudentDAO()
        students = dao.getStudentsByMentorId(mentor_id)
        result = []
        if not students:
            return jsonify(Error="NOT FOUND"), 404
        course_handler = CourseHandler()
        task_handler = TaskHandler()
        for s in students:
            student = self.dicStudent(s)

            # get student's courses
            # handler will return a tuple, first element is the response, second element is response status
            courses = course_handler.get_courses_with_grades_by_student_id(student['user_id'])
            # if response status is 200 it means there is a result, otherwise no result was found and will be ignored
            if courses[1] is 200:
                # response is jsonified, need to get json
                student['courses'] = courses[0].get_json()

            # get student's tasks
            tasks = task_handler.get_all_tasks_by_user_id(student['user_id'])
            if tasks[1] is 200:
                student['tasks'] = tasks[0].get_json()

            result.append(student)
        return jsonify(result), 200

    def getStudent(self, user_id):
        student = StudentDAO().getStudent(user_id)
        if not student:
            return jsonify(Error='NOT FOUND'), 404
        return jsonify(self.dicStudent(student)), 200

    # PUT Methods

    def changePhoneNum(self, user_id, phone):
        response = StudentDAO().changePhoneNumber(phone, user_id)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0], 'new_phone_num': response[1]}
        return jsonify(result=result), 200

    def changeStudentNum(self, user_id, student_num):
        response = StudentDAO().changeStundentNumber(student_num, user_id)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0], 'new_phone_num': response[1]}
        return jsonify(result=result), 200

    def changeProgram(self, user_id, program):
        response = StudentDAO().changeProgram(program, user_id)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0], 'new_phone_num': response[1]}
        return jsonify(result=result), 200

    def changeName(self, user_id, name):
        response = StudentDAO().changeName(name, user_id)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0], 'new_name': response[1]}
        return jsonify(result=result), 200

    def changeLastname(self, user_id, lastname):
        response = StudentDAO().changeLastname(lastname, user_id)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0], 'new_lastname': response[1]}
        return jsonify(result=result), 200

    def changeUsername(self, user_id, username):
        response = StudentDAO().changeUsername(username, user_id)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0], 'new_username': response[1]}
        return jsonify(result=result), 200

    def changeEmail(self, user_id, email):
        response = StudentDAO().changeEmail(email, user_id)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0], 'new_email': response[1]}
        return jsonify(result=result), 200

    def changePassword(self, user_id, password):
        response = StudentDAO().changePassword(password, user_id)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0]}
        return jsonify(result=result), 200