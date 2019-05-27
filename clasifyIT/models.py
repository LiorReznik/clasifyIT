from flask_login import UserMixin
import base64
import onetimepass
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .encrypt import hash
db = SQLAlchemy()
login_manager = LoginManager()
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

key='5791628bb0b13ce0c676dfde280ba245'

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

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.second_factor_c:
            # generate a random secret
            self.second_factor_c = base64.b32encode(os.urandom(10)).decode('utf-8')

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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(key, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None


        return User.query.get(user_id)