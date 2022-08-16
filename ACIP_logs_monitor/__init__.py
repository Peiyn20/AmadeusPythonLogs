from flask import Flask, app, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
import config
from datetime import timedelta


db = SQLAlchemy()
DB_NAME = config.DB_URI


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    db.init_app(app)
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):

        return User.query.get(int(id))
    return app


def create_database(app):
    if not path.exists("db/" + DB_NAME):
        db.create_all(app=app)
        print("DB created")
