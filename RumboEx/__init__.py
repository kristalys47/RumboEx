from flask import Flask, request, render_template, redirect, url_for, current_app, g, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, fresh_login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_rbac import RBAC
from flask_cors import CORS, cross_origin
from RumboEx.handler.StudentHandler import StudentHandler



#from flask_jwt_extended import JWTManager

# This code must be un once two create the tables in the DataBase
# User.metadata.create_all(engine)
# Role.metadata.create_all(engine)
# db.create.all()

# Staring Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
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
    remember = BooleanField('remenber me')

@app.route('/')
@rbac.exempt
@login_required
def hello_world():
    return 'Bienvenidos a RumboEx ToDo'


@app.route('/current')
@rbac.exempt
@login_required
def current():
    global current_user
    print(current_user)
    return "esta en al pantalla de python el current user"

@app.route('/users')
@rbac.allow(['admin'], ['GET'], with_children=False)
@login_required
def getallusers():
    handler = StudentHandler()
    return handler.getallusers()


@app.route('/createuser/<string:username>/<string:email>/<string:password>/<string:name>/<string:lastname>/<int:program>/<int:student_num>', methods=['GET'])
@rbac.allow(['admin'], ['GET'], with_children=False)
@login_required
def createStudent(username, email, password, name, lastname, program, student_num):
    student = StudentHandler()
    return student.insertStudent(username, email, password, name, lastname, program, student_num)


@app.route('/login', methods=['GET', 'POST'])
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
                print(user.roles)
                login_user(user, True)
                current_user = user
                return jsonify(Result="Successful"), 200
            else:
                return jsonify(Result="Not same password"), 400
        return jsonify(Result="This user does not exist in the data base"), 400
    return jsonify(Result="is not a Post method, but returns"), 200


# Routes to test the identification of a user
# @app.route('/loginStudent', methods=['GET'], )
# @rbac.allow(['Student'], ['GET'])
# def confirmStudent():
#     return "Hi: This programs tells me that you are a Student"
#
#
# @app.route('/loginMentor', methods=['GET'])
# @rbac.allow(['Mentor'], ['GET'])
# def confirmMentor():
#     return "Hi: This programs tells me that you are a Mentor"
#
#
# @app.route('/loginCounselor', methods=['GET'])
# @rbac.allow(['Counselor'], ['GET'])
# def confirmCounselor():
#     return "Hi: This programs tells me that you are a Counselor"
#
#
# @app.route('/loginAdmin', methods=['GET'])
# @rbac.allow(['Admin'], ['GET'])
# def confirmAdmin():
#     return "Hi: This programs tells me that you are a Admin"


@app.route('/logout', methods=['GET'])
@rbac.exempt
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/calendar')
@rbac.allow(['student'], ['GET'])
@login_required
def calendar():
    global current_user
    print(current_user.roles)
    return render_template('calendar.html')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
