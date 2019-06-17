from flask_login import UserMixin
import base64
import onetimepass
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .encrypt import hash, HMAC
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import base64
from clasifyIT import config
from flask import session
from secrets import token_bytes

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    firstName=db.Column(db.String(20))
    lastName=db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    second_factor_c = db.Column(db.String(16))
    email = db.Column(db.String(64), unique=True, index=True)
    hasher = hash.hasher()
    salt = db.Column(db.String(8), unique=True)
    admin=db.Column(db.Boolean(),default=False)

    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.second_factor_c:
            # generate a random secret
            self.second_factor_c = base64.b32encode(os.urandom(10)).decode('utf-8')
        if not self.salt:
            self.salt = base64.b32encode(os.urandom(4)).decode('utf-8')

    @property
    def password(self):pass

    @password.setter
    def password(self, password):
        self.password_hash= self.hasher['hash'](password)

    def verify_password(self, password):
        return self.hasher['check'](self.password_hash, password)

    def get_otp_uri(self):
        return 'otpauth://totp/2FA-ClassifyIT:{0}?secret={1}&issuer=2FA-ClassifyIT' \
            .format(self.username, self.second_factor_c)

    def verify_otp(self, token):
        return onetimepass.valid_totp(token, self.second_factor_c)

    def make_hmac(self):
        
        return HMAC.hmac(self.salt, str(self.id))#sending the salt and id of user to ths hmac maker

    def verify_code(self, code):
        
        return HMAC.check_authentication(self.salt, str(self.id), code) #veifing the auth code for  verification


    def get_reset_token(self, expires_sec=1800):
        self.create_token()
        s = Serializer(session['key'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def create_token(self):
        session['key'] = token_bytes()

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(session['key'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)