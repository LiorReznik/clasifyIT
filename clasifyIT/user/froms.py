from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo,Regexp


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
    firstName=StringField('First Name',validators=[DataRequired()])
    lastName=StringField('Last Name',validators=[DataRequired()])
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