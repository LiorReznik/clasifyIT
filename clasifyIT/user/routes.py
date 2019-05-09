from flask import Blueprint
from flask_login import login_user, logout_user, \
    current_user
from flask import render_template, redirect, url_for, flash, session, \
    abort
from .froms import SingupForm, LoginForm, OtaloginForm
from io import BytesIO
from ..models import User , db
import pyqrcode

users = Blueprint('users', __name__)


@users.route('/singup', methods=['GET', 'POST'])
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
        return redirect(url_for('home.index'))

    form = SingupForm()
    if form.validate_on_submit():
        msg = ''
        validate_reg()
        if len(msg) > 0:
            flash(msg)
            return redirect(url_for('users.singup'))
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        return redirect(url_for('users.two_factor_setup'))
    return render_template('singup.html', form=form)


@users.route('/twofactor')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('home.index'))
    user = User.query.filter_by(username=session['username']).first()
    if not user :
        return redirect(url_for('home.index'))
    return render_template('2FA_reg.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@users.route('/qrcode')
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


@users.route('/login', methods=['GET', 'POST'])
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
        return redirect(url_for('home.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        msg = ''
        login_verify()
        if len(msg) > 0:
            flash(msg)
            return redirect(url_for('users.login'))

        session['username'] = user.username ; session['type'] = 'login'
        return redirect(url_for('users.two_factor_token'))
    return render_template('login.html', form=form)

@users.route('/token', methods=[ 'get', 'post'])
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
                return redirect(url_for('users.two_factor_token'))
            login()
            return redirect(url_for('home.index'))

    return render_template('2FA.html', form=form)

@users.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    return redirect(url_for('home.index'))
