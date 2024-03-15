from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from myapp.config import Config
from myapp.database import db
from flask_login import LoginManager

socket = SocketIO()
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    socket.init_app(app, cors_allowed_origins="*")
    cors.init_app(app)

    from .database import User

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Register blueprints
        from .views import views
        app.register_blueprint(views)

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app, socket

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from os import path
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from flask_login import LoginManager

# db = SQLAlchemy()
# DB_NAME = "database.db"


# socket = SocketIO()
# cors = CORS()

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
#     app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
#     db.init_app(app)
#     socket.init_app(app, cors_allowed_origins="*")
#     cors.init_app(app)

#     from .views import views
#     from .auth import auth

#     app.register_blueprint(views, url_prefix='/')
#     app.register_blueprint(auth, url_prefix='/')

#     from .models import User
    
#     with app.app_context():
#         db.create_all()

#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#     login_manager.init_app(app)

#     @login_manager.user_loader
#     def load_user(id):
#         return User.query.get(int(id))

#     return app, socket


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')