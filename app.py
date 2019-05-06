from flask_migrate import Migrate
import os
import base64
from io import BytesIO
from flask import Flask, render_template, redirect, url_for, flash, session, \
    abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo,Regexp
import onetimepass
import pyqrcode

# create application instance
app = Flask(__name__)
app.config.from_object('config')

# initialize extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = LoginManager(app)


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    second_factor_c = db.Column(db.String(16))
    email = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.second_factor_c:
            # generate a random secret
            self.second_factor_c = base64.b32encode(os.urandom(10)).decode('utf-8')

    @property
    def password(self):pass

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_otp_uri(self):
        return 'otpauth://totp/2FA-ClassifyIT:{0}?secret={1}&issuer=2FA-ClassifyIT' \
            .format(self.username, self.second_factor_c)

    def verify_otp(self, token):
        return onetimepass.valid_totp(token, self.second_factor_c)


@manager.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login."""
    return User.query.get(int(user_id))


class SingupForm(FlaskForm):
    """Registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Username must contain only letters, numbers, dots or underscores') ])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Regexp(
                                                    "^(?=.{8,})(?=.*[1-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[(!@#$%^&*()_+|~\- =\`{}[\]:”;'<>?,.\/, )])(?!.*(.)\1{2,}).+$",
                                                         0, "Password must contain at least 8 chars, at least one digit, at least one lowercase, at least one uppercase, at leatet one speacial char and without sequencial repeats"







                                                     )])
    password2 = PasswordField('Password2',
                              validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sumbit')


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class OtaloginForm(FlaskForm):
    """Second factor authentication login"""
    token = StringField('Token', validators=[DataRequired(), Length(6, 6)])
    submit = SubmitField('Login')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    """User registration route."""
    def validate_reg():
        """""
        validate that the username or email does not in the database 
        """""
        nonlocal msg
        email = User.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            msg += 'Username already exists.\n'
        if email:
            msg += 'Email already exists.\n'


    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SingupForm()
    if form.validate_on_submit():
        msg = ''
        validate_reg()
        if len(msg) > 0:
            flash(msg)
            return redirect(url_for('singup'))
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        return redirect(url_for('two_factor_setup'))
    return render_template('singup.html', form=form)


@app.route('/twofactor')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=session['username']).first()
    if not user :
        return redirect(url_for('index'))
    return render_template('2FA_reg.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        abort(404)

    del session['username']

    url = pyqrcode.create(user.get_otp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    def login_verify():
        nonlocal msg
        if not user:
            msg += 'Wrong username'
            return
        if not user.verify_password(form.password.data):
            msg += 'Wrong password'

    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        msg = ''
        login_verify()
        if len(msg) > 0:
            flash(msg)
            return redirect(url_for('login'))

        session['username'] = user.username ; session['type'] = 'login'
        return redirect(url_for('two_factor_token'))
    return render_template('login.html', form=form)

@app.route('/token', methods=[ 'get', 'post'])
def two_factor_token( ):
    def delsession():
        del session['username'] ; del session['type']



    def login():
        login_user(user)
        flash('Login was successful')
        delsession()

    form = OtaloginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        if session['type']  == 'login':
            if not user.verify_otp(form.token.data):
                flash('Token is wrong!')
                return redirect(url_for('two_factor_token'))
            login()
            return redirect(url_for('index'))

    return render_template('2FA.html', form=form)

@app.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    return redirect(url_for('index'))


db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
