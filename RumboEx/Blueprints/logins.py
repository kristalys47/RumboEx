from flask import jsonify, request, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from RumboEx import rbac
from flask_cors import cross_origin
from RumboEx.handler.StudentHandler import StudentHandler

from RumboEx.model.user import User
from RumboEx.model.role import Role


logins = Blueprint('logins', __name__)


class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
    remember = BooleanField('remember me')


@logins.route('/logout', methods=['GET', 'POST'])
@rbac.exempt
def logout():
    logout_user()
    return jsonify(result="Successful"), 200


@logins.route('/adminlogin', methods=['POST'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def adminlogin():
    return login(request, 'admin')


@logins.route('/studentlogin', methods=['POST'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def studentlogin():
    return login(request, 'student')


@logins.route('/counselorlogin', methods=['POST'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def counselorlogin():
    return login(request, 'counselor')


@logins.route('/psychologistlogin', methods=['POST'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def psychologistlogin():
    return login(request, 'psychologist')


@logins.route('/mentorlogin', methods=['POST'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def mentorlogin():
    return login(request, 'mentor')


@logins.route('/professorlogin', methods=['POST'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def professorlogin():
    return login(request, 'professor')


@logins.route('/advisorlogin', methods=['POST'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def advisorlogin():
    return login(request, 'advisor')


# This will be the standard login. Should not be used.
@logins.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def loginuser():
    if request.method == 'POST':
        credential = request.get_json()
        # Queries for user in database. Since usernames are unique, if it exists in db it should be the first appearance
        # TODO: consider login options with other fields other that username (ex: email)
        user = User.query.filter_by(username=credential['username']).first()
        print(user.object())
        if user:
            global current_user
            # Check if password is valid
            if check_password_hash(user.password, credential['password']):
                try:
                    remember = credential['remember']
                except:
                    # If remember field is null, set default to false
                    remember = False
                login_user(user, remember)
                return jsonify(result=user.object()), 200

            return jsonify(result="Invalid password"), 401
        return jsonify(result="User not found"), 401
    return jsonify(result="Is not a Post method, but returns"), 200


def login(request, role):
    if request.method == 'POST':
        credential = request.get_json()
        # Queries for user in database. Since usernames are unique, if it exists in db it should be the first appearance
        # TODO: consider login options with other fields other that username (ex: email)
        user = User.query.filter_by(username=credential['username']).first()
        print(user.object())
        if user:
            # Check if user role matches with the page trying to login to
            if user.object()['roles'][0] == role:
                global current_user
                # Check if password is valid
                if check_password_hash(user.password, credential['password']):
                    try:
                        remember = credential['remember']
                    except:
                        # If remember field is null, set default to false
                        remember = False
                    login_user(user, remember)
                    return jsonify(result=user.object()), 200

                return jsonify(result="Invalid password"), 401
            return jsonify(result="User trying to login to unathorized page"), 401
        return jsonify(result="User not found"), 401
    return jsonify(result="Is not a Post method, but returns"), 200
