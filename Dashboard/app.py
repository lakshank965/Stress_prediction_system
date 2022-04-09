import os

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine

# from Operations import connect_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# database connection to dashboard login
DB_URI = "mongodb+srv://dashboard-login:zKRPxnKYDGfSiPNA@spm-cluster.g8ddv.mongodb.net/spmdb?retryWrites=true&w=majority"
app.config['MONGODB_SETTINGS'] = {'host': os.environ.get('MONGODB_URI', DB_URI)}
db = MongoEngine(app)


class DashboardUser(db.Document, UserMixin):
    emp_id = db.StringField(required=True, unique=True, max_length=40, index=True)
    # name = db.StringField(required=False, max_length=80, index=True)
    # email = db.EmailField(unique=True, required=False, sparse=True, max_length=80, index=True)
    password = db.StringField(required=False, index=True)


@login_manager.user_loader
def load_user(user_id):
    """Load the user object from the user ID stored in the session"""
    return DashboardUser.objects(pk=user_id).first()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4)])
    remember = BooleanField('remember me')


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    dashboard_user = ''
    form = LoginForm()

    if form.validate_on_submit():
        user = DashboardUser.objects(emp_id=form.username.data).first()

        if user:
            if user.password == form.password.data:
                # if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                # return redirect(url_for('dashboard'))
                return '<h1>user login success</h1>'

        return f'<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
