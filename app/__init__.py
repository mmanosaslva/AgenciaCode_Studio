import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_name='development'):
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'test-secret-key'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['MAIL_SUPPRESS_SEND'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL',
            'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'agenciacode.db')
        )
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.permanent_session_lifetime = timedelta(days=30)

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from app.models.user import User
        from app.models.client import Client
        from app.models.collaborator import Collaborator
        from app.models.project import Project
        from app.models.task import Task
        from app.models.assignment import CollaboratorProject
        from app.database.models import PasswordResetToken

        if config_name != 'testing':
            from app.database import models as _models
            db.create_all()

    from app.routes import web_bp
    app.register_blueprint(web_bp)

    return app
