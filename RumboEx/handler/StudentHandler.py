from RumboEx.dao.StudentDAO import StudentDAO
from RumboEx.dao.CourseDao import CourseDAO
from RumboEx.dao.taskDao import TaskDAO
from RumboEx.handler.CourseHandler import CourseHandler
from flask import jsonify

class StudentHandler:

    def dicUser(self, user):
        return {'user_id': user[0], 'username': user[1], 'name': user[2], 'lastname': user[3]}

    def dicStudent(self, student):
        return {'name': student[0], 'lastname': student[1], 'username': student[2], 'user_id': student[3], 'email': student[4], 'password': student[5], 'student_num': student[6], 'enrolled_program': student[7], 'role_name': student[8], 'role_id': student[9], 'program_name': student[10], 'department_name': student[11], 'department_num': student[12]}

    def dicUser(self, user):
        return {'user_id': user[0], 'username': user[1], 'name': user[2], 'lastname': user[3]}

    def insertStudent(self, username, email, password, name, lastname, program, student_num):
        calltoInsert = StudentDAO().insertStudent(username, email, password, name, lastname, program, student_num)
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
            if courses.response is 200:
                print(courses.status_code)
                student['courses'] = courses.status_code
            # student['tasks'] = TaskDAO().get
            mapped_result.append(student)
        print(mapped_result)
        return jsonify(mapped_result), 200


    def getStudent(self, user_id):
        student = StudentDAO().getStudent(user_id)
        if not student:
            return jsonify(Error='NOT FOUND'), 404
        return jsonify(self.dicStudent(student)), 200
