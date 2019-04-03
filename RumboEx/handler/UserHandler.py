from flask import jsonify
from RumboEx.dao.UserDao import UserDAO


class UserHandler:

    # POST Methods

    def insertCounselor(self, username, email, password, name, lastname):
        calltoInsert = UserDAO().insertCounselor(username, email, password, name, lastname)
        return jsonify(result=calltoInsert), 200

    def insertPsychologist(self, username, email, password, name, lastname):
        calltoInsert = UserDAO().insertPsychologist(username, email, password, name, lastname)
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
