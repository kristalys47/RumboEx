from flask import jsonify, request, Blueprint
from flask_rbac import RBAC
from flask_cors import CORS, cross_origin
from RumboEx.handler.UserHandler import UserHandler

users = Blueprint('user_page', __name__)
CORS(users)

@users.route('/user/<int:user_id>', methods=['OPTIONS', 'PUT'])
@cross_origin()
def get_user(user_id):
    if request.method == 'PUT':
        cred = request.get_json()
        if 'email' in cred:
            return UserHandler().changeEmail(user_id, cred['email'])
        if 'username' in cred:
            return UserHandler().changeUsername(user_id, cred['username'])
        if 'password' in cred:
            return UserHandler().changePassword(user_id, cred['password'])
