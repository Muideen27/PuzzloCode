from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import timedelta
from flask_mail import Mail

db = SQLAlchemy()

mail = Mail() # creating Mail instance

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PuzzloCode'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
    # Initialize extensions
    db.init_app(app)

    # session timeout
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    # Keep Sessions Alive
    @app.before_request
    def session_timeout():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=1)  # Set your preferred session timeout

    # Configuration for Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'mycolorfullife27@gmail.com'
    app.config['MAIL_PASSWORD'] = os.environ.get("FLASK_APP_PASSWORD")
    app.config['MAIL_DEBUG'] = True

    mail = Mail(app) # creating Mail instance

    # Registering all blueprints
    from .views import views
    from .auth import auth
    from .assessment import assessment

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(assessment, url_prefix='/')

    from .models import User

    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all(app=app)
        print('Created Database!')