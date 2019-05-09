from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask import Flask
from .config import Config
from flask_mail import Mail
from .user.routes import users
from .home.routes import home
from .models import  db , login_manager

mail = Mail()


def create_app(config_class = Config):
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.register_blueprint(users)
    app.register_blueprint(home)
    bootstrap = Bootstrap(app)
    migrate = Migrate(app, db)
    return app






