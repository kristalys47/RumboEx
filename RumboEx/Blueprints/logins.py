from flask import jsonify, request, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from RumboEx import rbac
from flask_cors import cross_origin
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


@logins.route('/adminlogin', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@rbac.exempt

def adminlogin():
    if request.method == 'POST':
        credential = request.get_json()
        print(request)
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            if user.object()['roles'][0] == 'admin':
                global current_user
                hashed_password = generate_password_hash(user.password, method='sha256')
                if check_password_hash(hashed_password, credential['password']):
                    print(user.object())
                    try:
                        remember = credential['remember']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="Invalid password"), 401
            return jsonify(result="Role not valid"), 401
        return jsonify(result="User object null"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@logins.route('/studentlogin', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def studentlogin():
    if request.method == 'POST':
        credential = request.get_json()
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            if user.object()['roles'][0] == 'student':
                global current_user
                hashed_password = generate_password_hash(user.password, method='sha256')
                if check_password_hash(hashed_password, credential['password']):
                    print(user.object())
                    try:
                        remember = credential['remember']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="Invalid password"), 401
            return jsonify(result="Role not valid"), 401
        return jsonify(result="User object null"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@logins.route('/counselorlogin', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def counselorlogin():
    if request.method == 'POST':
        credential = request.get_json()
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            if user.object()['roles'][0] == 'counselor':
                global current_user
                hashed_password = generate_password_hash(user.password, method='sha256')
                if check_password_hash(hashed_password, credential['password']):
                    print(user.object())
                    try:
                        remember = credential['remember']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="Invalid password"), 401
            return jsonify(result="Role not valid"), 401
        return jsonify(result="User object null"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@logins.route('/psychologistlogin', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def psychologistlogin():
    if request.method == 'POST':
        credential = request.get_json()
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            if user.object()['roles'][0] == 'psychologist':
                global current_user
                hashed_password = generate_password_hash(user.password, method='sha256')
                if check_password_hash(hashed_password, credential['password']):
                    print(user.object())
                    try:
                        remember = credential['remember']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="Invalid password"), 401
            return jsonify(result="Role not valid"), 401
        return jsonify(result="User object null"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@logins.route('/mentorlogin', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def mentorlogin():
    if request.method == 'POST':
        credential = request.get_json()
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            print(user.object()['roles'])
            if user.object()['roles'][0] == 'mentor':
                global current_user
                hashed_password = generate_password_hash(user.password, method='sha256')
                if check_password_hash(hashed_password, credential['password']):
                    print(user.object())
                    try:
                        remember = credential['remember']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="Invalid password"), 401
            return jsonify(result="Role not valid"), 401
        return jsonify(result="User object null"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@logins.route('/professorlogin', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def professorlogin():
    if request.method == 'POST':
        credential = request.get_json()
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            if user.object()['roles'][0] == 'professor':
                global current_user
                hashed_password = generate_password_hash(user.password, method='sha256')
                if check_password_hash(hashed_password, credential['password']):
                    print(user.object())
                    try:
                        remember = credential['remember']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="Invalid password"), 401
            return jsonify(result="Role not valid"), 401
        return jsonify(result="User object null"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@logins.route('/advisorlogin', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def advisorlogin():
    if request.method == 'POST':
        credential = request.get_json()
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            if user.object()['roles'][0] == 'advisor':
                global current_user
                hashed_password = generate_password_hash(user.password, method='sha256')
                if check_password_hash(hashed_password, credential['password']):
                    print(user.object())
                    try:
                        remember = credential['remember']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="Invalid password"), 401
            return jsonify(result="Role not valid"), 401
        return jsonify(result="User object null"), 401
    return jsonify(result="is not a Post method, but returns"), 200


# This will be the standard login
@logins.route('/login', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@rbac.exempt
def login():
    if request.method == 'POST':
        credential = request.get_json()
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            global current_user
            hashed_password = generate_password_hash(user.password, method='sha256')
            if check_password_hash(hashed_password, credential['password']):
                print(user.object())
                try:
                    remember = credential['remember']
                except:
                    remember = False
                ret = login_user(user, remember)
                print(ret)
                current_user = user
                return jsonify(result=user.object()), 200
            else:
                return jsonify(result="Invalid password"), 401
        return jsonify(result="User object null"), 401
    return jsonify(result="is not a Post method, but returns"), 200
