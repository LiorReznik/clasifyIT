from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import onetimepass
import os

db = SQLAlchemy()

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