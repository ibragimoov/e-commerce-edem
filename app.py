from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edemiko.db'
    app.secret_key = 'some'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)

    bcrypt = Bcrypt()

    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app