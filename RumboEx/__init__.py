from flask import Flask, request, render_template, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from RumboEx.dao.StudentDAO import StudentDAO
from RumboEx.dao.taskDao import TaskDAO

from RumboEx.handler.taskHandler import TaskHandler

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_rbac import RBAC
from flask_cors import CORS, cross_origin
from RumboEx.handler.StudentHandler import StudentHandler
# from flask_jwt_extended import JWTManager

# This code must be un once two create the tables in the DataBase
# User.metadata.create_all(engine)
# Role.metadata.create_all(engine)
# db.create.all()

# Staring Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# Set RBAC to negative logic(All roles are block unless allowed or exempt)
app.config['RBAC_USE_WHITE'] = True
app.debug = True
CORS(app)

# DB info
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ivbustqhsmsaps:7a8951928430c500e432dbf97728f42f5033648c052a5befce59295cabd987c5@ec2-23-21-216-174.compute-1.amazonaws.com:5432/d9t2kdqh5u8ekk'
engine = create_engine('postgres://ivbustqhsmsaps:7a8951928430c500e432dbf97728f42f5033648c052a5befce59295cabd987c5@ec2-23-21-216-174.compute-1.amazonaws.com:5432/d9t2kdqh5u8ekk', echo=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


# If this imports are done before a circle dependency is created and the app will not run.
from RumboEx.model.role import Role
from RumboEx.model.user import User

# NPI
# jwt = JWTManager(app)

rbac = RBAC(app)
rbac.set_user_loader(lambda: current_user)
rbac.set_user_model(User)
rbac.set_role_model(Role)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initial role for RBAC to work
start = Role('DUMMY')
rbacDummy = User(roles=[start])

# To use this variable write global before the name in the methods
current_user = rbacDummy


class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
    remember = BooleanField('remember me')

@app.route('/')
@rbac.exempt
def hello_world():
    return 'Bienvenidos a RumboEx ToDo'


@app.route('/current')
@rbac.allow(['admin'], ['GET', 'POST'], with_children=False)
def current():
    global current_user
    print(current_user.object())
    return "esta en al pantalla de python el current user"

@app.route('/users')
@rbac.allow(['admin'], ['GET'], with_children=False)
def getallusers():
    handler = StudentHandler()
    return handler.getallusers()

@app.route('/student', methods=['POST', 'GET'])
@rbac.allow(['admin', 'counselor', 'advisor'], ['GET'], with_children=False)
def getallstudents():
    handler = StudentHandler()
    return handler.getallstudent()


@app.route('/register', methods=['POST', 'GET', 'OPTIONS'])
@rbac.allow(['admin'], ['GET', 'POST', 'OPTIONS'], with_children=False)
def createStudent():
    if request.method == 'POST':
        cred = request.form
        print(cred)
        username = cred['email'].split('@')[0]
        email = cred['email']
        name = cred['name']
        lastname = cred['lastname']
        program = cred['program']
        password = cred['password']
        student_num = cred['student_num']
        student = StudentHandler()
        print("Entra a la ruta")
        return student.insertStudent(username, email, password, name, lastname, program, student_num)
    print("Entra a la ruta")
    return jsonify(result="is not a Post method, but returns"), 200

@app.route('/adminlogin', methods=['POST', 'GET'])
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
                        remember = credential['remenber']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="There is an error"), 401
            return jsonify(result="There is an error"), 401
        return jsonify(result="There is an error"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/studentlogin', methods=['POST', 'GET'])
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
                        remember = credential['remenber']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="There is an error"), 401
            return jsonify(result="There is an error"), 401
        return jsonify(result="There is an error"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/counselorlogin', methods=['POST', 'GET'])
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
                        remember = credential['remenber']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="There is an error"), 401
            return jsonify(result="There is an error"), 401
        return jsonify(result="There is an error"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/mentorlogin', methods=['POST', 'GET'])
@rbac.exempt
def mentorlogin():
    if request.method == 'POST':
        credential = request.get_json()
        print(credential)
        user = User.query.filter_by(username=credential['username']).first()
        if user:
            if user.object()['roles'][0] == 'mentor':
                global current_user
                hashed_password = generate_password_hash(user.password, method='sha256')
                if check_password_hash(hashed_password, credential['password']):
                    print(user.object())
                    try:
                        remember = credential['remenber']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="There is an error"), 401
            return jsonify(result="There is an error"), 401
        return jsonify(result="There is an error"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/professorlogin', methods=['POST', 'GET'])
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
                        remember = credential['remenber']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="There is an error"), 401
            return jsonify(result="There is an error"), 401
        return jsonify(result="There is an error"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/advisorlogin', methods=['POST', 'GET'])
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
                        remember = credential['remenber']
                    except:
                        remember = False
                    ret = login_user(user, remember)
                    print(ret)
                    current_user = user
                    return jsonify(result=user.object()), 200
                else:
                    return jsonify(result="There is an error"), 401
            return jsonify(result="There is an error"), 401
        return jsonify(result="There is an error"), 401
    return jsonify(result="is not a Post method, but returns"), 200


# This will be the standard login
@app.route('/login', methods=['POST', 'GET'])
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
                return jsonify(result="There is an error"), 401
        return jsonify(result="There is an error"), 401
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/logout', methods=['GET', 'POST'])
@rbac.exempt
def logout():
    logout_user()
    return jsonify(result="Successful"), 200
    # return redirect(url_for('login'))


@app.route('/calendar')
@rbac.allow(['student'], ['GET'])
def calendar():
    global current_user
    print(current_user.object())
    current_user = rbacDummy
    return render_template('calendar.html')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))



@app.route('/task/personal/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@rbac.allow(['student'], ['POST', 'GET'], with_children=False)
def get_personal_tasks(student_id):
    global current_user
    if request.method == 'GET':
        return TaskHandler().get_personal_task_by_user_id(student_id)
    elif request.method == 'POST':
        return TaskHandler().insert_personal_task(request.form)


@app.route('/task/study/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@rbac.allow(['student'], ['POST', 'GET'], with_children=False)
def get_study_tasks(student_id):
    return TaskHandler().get_study_task_by_user_id(student_id)


@app.route('/task/course/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@rbac.allow(['student'], ['POST', 'GET'], with_children=False)
def get_course_tasks(student_id):
    return TaskHandler().get_course_task_by_user_id(student_id)
    #


@app.route('/task/appointment/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@rbac.allow(['student'], ['POST', 'GET'], with_children=False)
def get_appointment_tasks(student_id):
    return TaskHandler().get_appointment_tasks_by_user_id(student_id)


@app.route('/task')
@rbac.allow(['student'], ['POST', 'GET'], with_children=False)
def get_all_tasks():
    return TaskHandler().get_all_tasks()

@app.route('/course/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@rbac.allow(['student'], ['POST', 'GET'], with_children=False)
def getcourses(student_id):
    return TaskHandler().get_courses(student_id)
