from flask import jsonify
from RumboEx.dao.UserDao import UserDAO


class UserHandler:

    def insertCounselor(self, username, email, password, name, lastname):
        calltoInsert = UserDAO().insertCounselor(username, email, password, name, lastname)
        return jsonify(result=calltoInsert), 200

    def insertPsychologist(self, username, email, password, name, lastname):
        calltoInsert = UserDAO().insertPsychologist(username, email, password, name, lastname)
        return jsonify(result=calltoInsert), 200