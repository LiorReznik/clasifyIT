from flask_login import UserMixin
import onetimepass
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .encrypt import hash, HMAC
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import session
from secrets import token_bytes

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model."""
    #  lines 21-31 is the db table config
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    second_factor_c = db.Column(db.String(16))
    email = db.Column(db.String(64), unique=True, index=True)
    hasher = hash.hasher()
    salt = db.Column(db.String(8), unique=True)
    admin = db.Column(db.Boolean(),default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):pass # here for the setter

    @password.setter
    def password(self, password):
        """
        setter for the password
        :param password:
        :return:
        """
        # storing hash of password and salt
        self.password_hash= self.hasher['hash'](password+self.salt)

    def verify_password(self, password):
        """
        verifing that the entered password  is actually users password
        :param password:
        :return:
        """
        # sending the hashed value that stored in the db and the entered password+ users salt to the hash checker
        return self.hasher['check'](self.password_hash, password+self.salt)

    def get_otp_uri(self):
        """
        making the otp uri for the qr
        :return:
        """
        return 'otpauth://totp/2FA-ClassifyIT:{}?secret={}&issuer=2FA-ClassifyIT'.format(self.username, self.second_factor_c)

    def verify_otp(self, token):
        """
        verifing the otp entered by user
        :param token:
        :return:
        """
        return onetimepass.valid_totp(token, self.second_factor_c)

    def make_hmac(self):
        """
        makeing hmac to send to the user
        :return:
        """
        # sending the salt and id of user to ths hmac maker
        return HMAC.hmac(self.salt, str(self.id))

    def verify_code(self, code):
        # veifing the auth code for  verification
        return HMAC.check_authentication(self.salt, str(self.id), code)


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