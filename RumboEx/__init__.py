from flask import Flask, request, render_template, redirect, url_for, current_app, g, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, fresh_login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_, ForeignKey
from sqlalchemy.orm import sessionmaker, relationships
from flask_rbac import RBAC, UserMixin, RoleMixin
from flask_cors import CORS
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
    print("current user id: " + str(user_id))
    print("current username: " + str(User.query.get(int(user_id)).username))
    print("current user roles: " + str(User.query.get(int(user_id)).roles))
    print(login_manager)
    # print(login_manager.current_user)
    print(current_user)
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
@rbac.allow(['admin'], ['GET'], with_children=False)
def current():
    global current_user
    print(current_user.object())
    return "esta en al pantalla de python el current user"

@app.route('/users')
@rbac.allow(['admin'], ['GET'], with_children=False)
@login_required
def getallusers():
    handler = StudentHandler()
    return handler.getallusers()


@app.route('/register', methods=['POST', 'GET'])
@rbac.allow(['admin'], ['POST', 'GET'], with_children=False)
def createStudent():
    if request.method == 'POST':
        cred = request.get_json()
        print(cred)
        username = cred['email'].split('@')[0]
        email = cred['email']
        name = cred['name']
        lastname = cred['lastname']
        program = cred['program']
        password = cred['password']
        student_num = cred['student_num']
        student = StudentHandler()
        return student.insertStudent(username, email, password, name, lastname, program, student_num)
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
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/logout', methods=['GET', 'POST'])
@rbac.exempt
def logout():
    logout_user()
    return jsonify(result="Successful"), 200
    # return redirect(url_for('login'))


@app.route('/calendar')
@rbac.allow(['student'], ['GET'])
@login_required
def calendar():
    global current_user
    global rbacDummy
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
def get_personal_tasks(student_id):
    if request.method == 'GET':
        print("llega")
        print("prueba: ")
        print(TaskHandler().get_personal_task_by_student_id(student_id).get_data())
        return TaskHandler().get_personal_task_by_student_id(student_id)
    elif request.method == 'POST':
        return TaskHandler().insert_personal_task(request.get_json())


@app.route('/task/study/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_study_tasks(student_id):
    return TaskHandler().get_study_task_by_student_id(student_id)


@app.route('/task/course/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_course_tasks(student_id):
    return TaskHandler().get_course_task_by_student_id(student_id)


@app.route('/task')
def get_all_tasks():
    return TaskHandler().get_all_tasks()
