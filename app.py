from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask import Flask
from user.routes import users
from home.routes import home
from models import db, User



# create application instance
app = Flask(__name__)
app.config.from_object('config')

# initialize extensions
bootstrap = Bootstrap(app)

migrate = Migrate(app, db)

manager = LoginManager(app)

app.register_blueprint(home)
app.register_blueprint(users)

db.init_app(app)

@manager.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login."""
    return User.query.get(int(user_id))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
