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
from __init__ import apps

# create application instance
app = apps

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







db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
