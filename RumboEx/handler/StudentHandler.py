from RumboEx.dao.StudentDAO import StudentDAO
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
        result = []
        for student in students:
            result.append(self.dicStudent(student))
        return jsonify(Users=result), 200

