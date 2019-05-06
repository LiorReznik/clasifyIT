from flask import Flask
from user.routes import mod as user
from home.routes import mod as home

apps = Flask(__name__)
apps.register_blueprint(home)
apps.register_blueprint(user, url_prefix='/user')
