from app import db, bcrypt
from app.database.models import User


class AuthController:

    @staticmethod
    def login(identificador, password):
        if not identificador or not password:
            return {'success': False, 'error': 'Usuario y contrasena son obligatorios'}
        user = User.query.filter((User.username == identificador) | (User.email == identificador)).first()
        if not user:
            return {'success': False, 'error': 'Credenciales invalidas'}
        if not bcrypt.check_password_hash(user.password_hash, password):
            return {'success': False, 'error': 'Credenciales invalidas'}
        return {'success': True, 'user': user}

    @staticmethod
    def create_user(username, password, role='user', name='', email=''):
        if not username or not password:
            return {'success': False, 'error': 'Usuario y contrasena son obligatorios'}
        if User.query.filter_by(username=username).first():
            return {'success': False, 'error': 'El usuario ya existe'}
        if email and User.query.filter_by(email=email).first():
            return {'success': False, 'error': 'El email ya esta registrado'}
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password_hash=password_hash, role=role, name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return {'success': True, 'message': 'Usuario creado exitosamente'}
