from flask import Blueprint,jsonify,request
from flask_login import login_user, logout_user, \
    current_user
from flask import render_template, redirect, url_for, flash, session, \
    abort
from .froms import SingupForm, LoginForm, OtaloginForm,RequestResetForm,ResetPasswordForm,ChangeUsername,ChangeName,ChangeEmail
from io import BytesIO
from ..models import User , db
import pyqrcode
from flask_mail import Message,Mail
from ..email import sender
from email.mime.text import MIMEText
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..encrypt import des_ofb,hash

users = Blueprint('users', __name__)


def check_email(email):
    users=User.query.all()
    flag=False
    for u in users:
        temp=des_ofb.ofb_decrypt(u.email,u.password_hash[:8],u.password_hash[24:32])
        if email in temp:
            flag=True
    return flag        


@users.route('/decrypted', methods=['GET'])
def decrypt_data():
    user=current_user
    email=des_ofb.ofb_decrypt(user.email,user.password_hash[:8],user.password_hash[24:32])
    firstName=des_ofb.ofb_decrypt(user.firstName,user.password_hash[:8],user.password_hash[24:32])
    lastName=des_ofb.ofb_decrypt(user.lastName,user.password_hash[:8],user.password_hash[24:32])
    return jsonify({'username': user.username,'email':email,'firstName':firstName,'lastName':lastName})

@users.route('/profile')
def profile():
    if current_user.is_authenticated:
        message="Hi There"
        return render_template('profile.html', message=message)
    else:
        return redirect(url_for('users.login'))
        
@users.route('/singup', methods=['GET', 'POST'])
def singup():
    """User registration route."""
    def validate_reg():
        """""
        validate that the username or email does not in the database 
        """""
        nonlocal msg
        email_ch=check_email(form.email.data)
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            msg += 'Username already exists.\n'
        if email_ch:
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
        email = form.email.data
        user = User(username=form.username.data, password=form.password.data, email=email,firstName=form.firstName.data,lastName=form.lastName.data)
        user.email=des_ofb.ofb_encrypt(user.email,user.password_hash[:8],user.password_hash[24:32])
        user.firstName=des_ofb.ofb_encrypt(user.firstName,user.password_hash[:8],user.password_hash[24:32])
        user.lastName=des_ofb.ofb_encrypt(user.lastName,user.password_hash[:8],user.password_hash[24:32])
        #send code to mail
        db.session.add(user)
        db.session.commit()
        sender.SendMail().preapare_attatched_mail(email,"Auth code","Your auth code is in the attachment",user.make_hmac())
        session['username'] = user.username
        return redirect(url_for('users.two_factor_setup'))
    return render_template('singup.html', form=form)

@users.route('/edit_username', methods=['GET', 'POST'])
def editProfile():
    if current_user.is_authenticated:

        """User registration route."""
        def validate_reg():
            """""
            validate that the username or email does not in the database 
            """""
            nonlocal msg
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                msg += 'Username already exists.\n'

        form = ChangeUsername()
        if form.validate_on_submit():
            msg = ''
            validate_reg()
            if len(msg) > 0:
                flash(msg)
                return redirect(url_for('users.editProfile'))

            current_user.username=form.username.data
            db.session.commit()
            return redirect(url_for('users.profile'))

        return render_template('edit-profile.html', form=form)
    else:
        return redirect(url_for('users.login'))

@users.route('/edit_name', methods=['GET', 'POST'])
def editName():
    if current_user.is_authenticated:
        form = ChangeName()
        if form.validate_on_submit():
            current_user.firstName=des_ofb.ofb_encrypt(form.firstName.data,current_user.password_hash[:8],current_user.password_hash[24:32])
            current_user.lastName=des_ofb.ofb_encrypt(form.lastName.data,current_user.password_hash[:8],current_user.password_hash[24:32])
            db.session.commit()
            return redirect(url_for('users.profile'))
        return render_template('edit-profile.html', form=form)
    else:
        return redirect(url_for('users.login'))

@users.route('/edit_email', methods=['GET', 'POST'])
def editEmail():
    if current_user.is_authenticated:

        """User registration route."""
        def validate_reg():
            """""
            validate that the username or email does not in the database 
            """""
            nonlocal msg
           
            email_ch = check_email(form.email.data)
            if email_ch:
                msg += 'Email already exists.\n'

        form = ChangeEmail()
        if form.validate_on_submit():
            msg = ''
            validate_reg()
            if len(msg) > 0:
                flash(msg)
                return redirect(url_for('users.editEmail'))
            current_user.email=des_ofb.ofb_encrypt(form.email.data,current_user.password_hash[:8],current_user.password_hash[24:32])
            db.session.commit()
            return redirect(url_for('users.profile'))
        return render_template('edit-profile.html', form=form)
    else:
        return redirect(url_for('users.login'))
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
def two_factor_token():
    def delsession():
        del session['username'] ; del session['type']

    def login():
        login_user(user)
        flash('Login was successful')
        delsession()

    def password_change():
        user.email=des_ofb.ofb_decrypt(user.email,user.password_hash[:8],user.password_hash[24:32])
        user.firstName=des_ofb.ofb_decrypt(user.firstName,user.password_hash[:8],user.password_hash[24:32])
        user.lastName=des_ofb.ofb_decrypt(user.lastName,user.password_hash[:8],user.password_hash[24:32])
        user.password = session['type'].decode()
        user.email=des_ofb.ofb_encrypt(user.email,user.password_hash[:8],user.password_hash[24:32])
        user.firstName=des_ofb.ofb_encrypt(user.firstName,user.password_hash[:8],user.password_hash[24:32])
        user.lastName=des_ofb.ofb_encrypt(user.lastName,user.password_hash[:8],user.password_hash[24:32])
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        delsession()

    form = OtaloginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        if session['type']  == 'login':
            if not user.verify_otp(form.token.data) or not user.verify_code(form.code.data): #check verificatio mail and  token
                flash('Token or auth code is Wrong!')
                return redirect(url_for('users.two_factor_token'))
            login()
            return redirect(url_for('home.index'))
        else:
            if not user.verify_otp(form.token.data) or not user.verify_code(form.code.data):
                flash('Token is wrong!')
                return redirect(url_for('users.two_factor_token'))
            password_change()
            return redirect(url_for('users.login'))

    return render_template('2FA.html', form=form)

@users.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    return redirect(url_for('home.index'))

def send_reset_email(user,email):
    token = user.get_reset_token()
    link = url_for('users.reset_token', token=token, _external=True)
    body = 'To reset your password, visit the following link: {} If you did not make this request then simply ignore this email and no changes will be made.'.format(
        link)

    msg = MIMEText(body, 'html')
    mail = sender.SendMail()
    mail.prepare_base_email(email, 'Password Reset Request', msg)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email=des_ofb.ofb_decrypt(user.email,user.password_hash[:8],user.password_hash[24:32])
        send_reset_email(user,email)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    #user=user = User.query.filter_by(salt=token).first()
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        session['username'] = user.username
        session['type'] = form.password.data.encode()
        email=des_ofb.ofb_decrypt(user.email,user.password_hash[:8],user.password_hash[24:32])
        sender.SendMail().preapare_attatched_mail(email, "Auth code", "Your auth code is in the attachment",user.make_hmac())
        
        return redirect(url_for('users.two_factor_token'))
    return render_template('reset_token.html', title='Reset Password', form=form)



