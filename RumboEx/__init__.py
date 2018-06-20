from flask import Flask, request, render_template, redirect, url_for, current_app, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_rbac import RBAC, UserMixin, RoleMixin

#from flask_jwt_extended import JWTManager

# This code must be un once two create the tables in the DataBase
# User.metadata.create_all(engine)
# Role.metadata.create_all(engine)

# Staring Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# app.config['RBAC_USE_WHITE'] = True
app.debug = True

# DB info
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ivbustqhsmsaps:7a8951928430c500e432dbf97728f42f5033648c052a5befce59295cabd987c5@ec2-23-21-216-174.compute-1.amazonaws.com:5432/d9t2kdqh5u8ekk'
engine = create_engine('postgres://ivbustqhsmsaps:7a8951928430c500e432dbf97728f42f5033648c052a5befce59295cabd987c5@ec2-23-21-216-174.compute-1.amazonaws.com:5432/d9t2kdqh5u8ekk', echo=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
login_manager.login_view = 'login'

# Esto esta super hardwire
start = Role('start')
anonymous = User(roles=[start])
current_user = anonymous

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_current_user():
    with app.request_context():
        return current_user

class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
    remember = BooleanField('remenber me')

@app.route('/')
@rbac.exempt
def hello_world():
    return 'Bienvenidos a RumboEx ToDo'

@app.route('/login', methods=['GET', 'POST'])
@rbac.allow(['everyone'], ['GET'], with_children=False)
def login():
    form = UserLoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user:
            hashed_password = generate_password_hash(user.password, method='sha256')
            if check_password_hash(hashed_password, form.password.data):
                print("AQUI 2")
                app.logger.debug('Logged in user %s', user.username)
                login_user(user, remember=form.remember.data)
                print(get_current_user())
                return redirect(url_for('calendar'))
        error = 'Invalid username or password.'
    elif request.method == "POST":
        flash_errors(form)
    return render_template('login.html', form=form, error=error)





# NPI
# hashed_password = generate_password_hash(form.password.data, method='sha56')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/calendar')
@login_required
@rbac.allow(['everyone'], ['GET'], with_children=False)
def calendar():
    return render_template('calendar.html')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

if __name__ == "__main__":
    app.run()