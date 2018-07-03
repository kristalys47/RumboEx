from RumboEx.dao.StudentDAO import StudentDAO
from flask import jsonify

class StudentHandler:

    def dicUser(self, user):
        return {'user_id': user[0], 'username': user[1], 'name': user[2], 'lastname': user[3]}

    def insertStudent(self, username, email, password, name, lastname, program, student_num):
        calltoInsert = StudentDAO().insertStudent(username, email, password, name, lastname, program, student_num)


    def getallusers(self):
        users = StudentDAO().getallusers()
        result = []
        for user in users:
            result.append(self.dicUser(user))
        return jsonify(Users=result), 200


