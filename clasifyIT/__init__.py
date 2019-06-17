from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask import Flask
from .config import Config
from .user.routes import users
from .home.routes import home
from .models import  db , login_manager,User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


def create_app(config_class = Config):
  
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(users)
    app.register_blueprint(home)
    bootstrap = Bootstrap(app)
    migrate = Migrate(app, db)
    class AdminModelView(ModelView):

        def is_accessible(self):
            return current_user.admin
            
    admin = Admin(app, name='clasifyIT', template_mode='bootstrap3')
    admin.add_view(AdminModelView(User, db.session))
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    return app






