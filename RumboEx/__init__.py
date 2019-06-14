from flask import Flask, request, render_template, jsonify
from flask_login import LoginManager, login_required, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from RumboEx.config.dbconfig import pg_config


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_rbac import RBAC
from flask_cors import CORS, cross_origin
# from flask_jwt_extended import JWTManager


# Handlers from Rest API
from RumboEx.handler.ProgramHandler import ProgramHandler
from RumboEx.handler.taskHandler import TaskHandler
from RumboEx.handler.StudentHandler import StudentHandler
from RumboEx.handler.CourseHandler import CourseHandler
from RumboEx.handler.MessageHandler import MessageHandler
from RumboEx.handler.AppointmentHandler import AppointmentHandler

from RumboEx.handler.UserHandler import UserHandler


# This code must be un once two create the tables in the DataBase
# User.metadata.create_all(engine)
# Role.metadata.create_all(engine)
# db.create.all()


# Staring Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# Set RBAC to negative logic(All roles are block unless allowed or exempt)
# app.config['RBAC_USE_WHITE'] = True
app.debug = True
CORS(app)
#CORS(app, support_credentials=True)

# DB info
app.config['SQLALCHEMY_DATABASE_URI'] = pg_config['url']
engine = create_engine(pg_config['url'], echo=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Session = sessionmaker(bind=engine) COMMENTED THIS ON MARCH 24 !!!!!!!!!!!!!!!!!!!!!!
#Session.configure(bind=engine)
#session = Session()


# If this imports are done before a circle dependency is created and the app will not run.
from RumboEx.model.role import Role
from RumboEx.model.user import User

# NPI
# jwt = JWTManager(app)

# Starting RBAC
rbac = RBAC()
rbac.init_app(app)
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
# login_manager.anonymous_user = rbacDummy


# Blueprints to import. Need to be after rbac
from RumboEx.Blueprints.logins import logins
from RumboEx.Blueprints.tasks import tasks
from RumboEx.Blueprints.courses import courses
from RumboEx.Blueprints.student_page import student_page
from RumboEx.Blueprints.appointments import appointments
from RumboEx.Blueprints.users import users

# Register blueprints
app.register_blueprint(logins)
app.register_blueprint(tasks)
app.register_blueprint(courses)
app.register_blueprint(student_page)
app.register_blueprint(appointments)
app.register_blueprint(users)

# from RumboEx.decorators.authorization import authorize

@app.route('/')
@rbac.exempt
# @authorize
def hello_world():
    return 'Bienvenidos a RumboEx ToDo'


@app.route('/current')
@login_required
# @rbac.allow(['admin'], ['GET'], with_children=False)
#@rbac.exempt
# @authorize
def current():
    global current_user
    print(current_user)
    return jsonify(current_user.object())
    # return "esta en al pantalla de python el current user"


@app.route('/register', methods=['POST', 'GET', 'OPTIONS'])
@rbac.allow(['admin'], ['GET', 'POST', 'OPTIONS'], with_children=False)
def createStudent():
    print(request)
    if request.method == 'POST':
        cred = request.get_json()
        print(cred)
        # username = cred['email'].split('@')[0]
        username = cred['username']
        email = cred['email']
        name = cred['name']
        lastname = cred['lastname']
        program = cred['program_num']
        password = generate_password_hash(cred['password'], method='sha256') # stores hashed password into db
        student_num = cred['student_num']
        phone_num = cred['phone_num']
        student = StudentHandler()
        return student.insertStudent(username, email, password, name, lastname, program, student_num, phone_num)
        # return CourseHandler().insert_course(user_id, cred)
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/register-counselor', methods=['POST', 'GET', 'OPTIONS'])
@rbac.allow(['admin'], ['GET', 'POST', 'OPTIONS'], with_children=False)
def createCounselor():
    print(request)
    if request.method == 'POST':
        cred = request.get_json()
        print(cred)
        # username = cred['email'].split('@')[0]
        username = cred['username']
        email = cred['email']
        name = cred['name']
        lastname = cred['lastname']
        password = generate_password_hash(cred['password'], method='sha256')
        user = UserHandler()
        return user.insertCounselor(username, email, password, name, lastname)
        # return CourseHandler().insert_course(user_id, cred)
    return jsonify(result="is not a Post method, but returns"), 200


@app.route('/register-psychologist', methods=['POST', 'GET', 'OPTIONS'])
@rbac.allow(['admin'], ['GET', 'POST', 'OPTIONS'], with_children=False)
def createPsychologist():
    print(request)
    if request.method == 'POST':
        cred = request.get_json()
        print(cred)
        # username = cred['email'].split('@')[0]
        username = cred['username']
        email = cred['email']
        name = cred['name']
        lastname = cred['lastname']
        password = generate_password_hash(cred['password'], method='sha256')
        user = UserHandler()
        return user.insertPsychologist(username, email, password, name, lastname)
        # return CourseHandler().insert_course(user_id, cred)
    return jsonify(result="is not a Post method, but returns"), 200


# esto es del ui viejo
@app.route('/calendar')
@rbac.allow(['student'], ['GET'])
@login_required
def calendar():
    global current_user
    print(current_user.object())
    # current_user = rbacDummy
    return render_template('calendar.html')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/messages/<int:user_id>', methods=['GET', 'POST', 'PUT'])
# @rbac.exempt
@rbac.allow(['student', 'mentor', 'counselor', 'psychologist'], ['GET', 'POST', 'PUT'], with_children=False)
@cross_origin()
def get_messages_by_user_id(user_id):
    if request.method == 'GET':
        return MessageHandler().get_chats_by_user_id(user_id)
    elif request.method == 'POST':
        return MessageHandler().insert_message(request.get_json())
    elif request.method == 'PUT':
        return MessageHandler().set_message_seen(request.get_json())

# @app.route('/messages/chat/<int:chat_id>', methods=['GET', 'POST'])
# def get_messages_by_chat_id(chat_id):
#     if request == 'GET':
#         return MessageHandler().get_chat_by_chat_id(chat_id)


@app.route('/faculties', methods=['GET'])
@rbac.exempt
def get_faculties():
    return ProgramHandler().get_faculties_and_programs()


# @app.route('/login', methods=['POST', 'GET'])
# @cross_origin(supports_credentials=True)
# @rbac.exempt
# def login():
#     if request.method == 'POST':
#         credential = request.get_json()
#         print(credential)
#         user = User.query.filter_by(username=credential['username']).first()
#         if user:
#             global current_user
#             if check_password_hash(user.password, credential['password']):
#                 print(user.object())
#                 try:
#                     remember = credential['remember']
#                 except:
#                     remember = False
#                 login_user(user, remember)
#                 print(current_user)
#                 # current_user = user
#                 print(current_user)
#                 return jsonify(result=user.object()), 200
#             else:
#                 return jsonify(result="Invalid password"), 401
#         return jsonify(result="User object null"), 401
#     return jsonify(result="is not a Post method, but returns"), 200
