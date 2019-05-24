from flask import jsonify
from RumboEx.dao.UserDao import UserDAO
from RumboEx.handler.emails import EmailHandler


class UserHandler:


    # GET Methods

    def getMnetorsByStudentId(self, student_id):
        dao = UserDAO()
        result = dao.getMentorsByStudentId(student_id)
        if not result:
            return jsonify(Error='NOT FOUND'), 404
        mapped_result = []
        for row in result:
            mapped_result.append(self.mapToUserLongDict(row))
        return jsonify(Mentors=mapped_result), 200

    # POST Methods

    def insertCounselor(self, username, email, password, name, lastname):
        calltoInsert = UserDAO().insertCounselor(username, email, password, name, lastname)
        EmailHandler().send_mail_after_register(calltoInsert)
        return jsonify(result=calltoInsert), 200

    def insertPsychologist(self, username, email, password, name, lastname):
        calltoInsert = UserDAO().insertPsychologist(username, email, password, name, lastname)
        EmailHandler().send_mail_after_register(calltoInsert)
        return jsonify(result=calltoInsert), 200

    # PUT Methods

    def changeEmail(self, user_id, email):
        response = UserDAO().changeEmail(user_id, email)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        print(response)
        result = {'user_id': response[0], 'new_email': response[1]}
        return jsonify(result=result), 200

    def changeUsername(self, user_id, username):
        response = UserDAO().changeUsername(user_id, username)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0], 'new_username': response[1]}
        return jsonify(result=result), 200

    def changePassword(self, user_id, password):
        response = UserDAO().changePassword(user_id, password)
        if not response:
            return jsonify(Error='USER NOT FOUND'), 404
        result = {'user_id': response[0]}
        return jsonify(result=result), 200

    # Map to dictionaries

    def mapToUserDict(self, row):
        return {
            'id': row[0],
            'username': row[1],
            'name': row[2],
            'lastname': row[3],
            'email': row[4],
            'password': row[5]
        }

    def mapToUserLongDict(self, row):
        return {
            'id': row[0],
            'username': row[1],
            'name': row[2],
            'lastname': row[3],
            'email': row[4],
            'role_id': row[5],
            'role_name': row[6]
        }

