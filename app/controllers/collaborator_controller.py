from app import db
from app.database.models import Collaborator
from app.utils.validators import validate_email, validate_required_fields
from app.utils.constants import ROLES, STATUS_COLABORADOR


class CollaboratorController:

    @staticmethod
    def get_all():
        return Collaborator.query.order_by(Collaborator.name).all()

    @staticmethod
    def get_by_id(collaborator_id):
        return Collaborator.query.get(collaborator_id)

    @staticmethod
    def get_available_for_project():
        all_collaborators = Collaborator.query.filter_by(status='activo').all()
        return [c for c in all_collaborators if c.can_assign_to_project()]

    @staticmethod
    def create(data):
        missing = validate_required_fields(data, ['name', 'role', 'email'])
        if missing:
            return {'success': False, 'error': f'Campos obligatorios faltantes: {", ".join(missing)}'}
        if data['role'] not in ROLES:
            return {'success': False, 'error': f'Rol invalido. Debe ser: {", ".join(ROLES)}'}
        if Collaborator.query.filter_by(email=data['email']).first():
            return {'success': False, 'error': 'El email ya esta registrado'}
        if not validate_email(data['email']):
            return {'success': False, 'error': 'Email invalido'}
        if 'status' in data and data['status'] and data['status'] not in STATUS_COLABORADOR:
            return {'success': False, 'error': f'Estado invalido. Debe ser: {", ".join(STATUS_COLABORADOR)}'}
        collab = Collaborator(
            name=data['name'],
            role=data['role'],
            status=data.get('status', 'activo'),
            email=data['email'],
            phone=data.get('phone'),
        )
        db.session.add(collab)
        db.session.commit()
        return {'success': True, 'message': 'Colaborador creado exitosamente', 'collaborator': collab}

    @staticmethod
    def update(collaborator_id, data):
        collab = Collaborator.query.get(collaborator_id)
        if not collab:
            return {'success': False, 'error': 'Colaborador no encontrado'}
        if 'name' in data and data['name']:
            collab.name = data['name']
        if 'role' in data:
            if data['role'] not in ROLES:
                return {'success': False, 'error': f'Rol invalido. Debe ser: {", ".join(ROLES)}'}
            collab.role = data['role']
        if 'status' in data:
            if data['status'] not in STATUS_COLABORADOR:
                return {'success': False, 'error': f'Estado invalido. Debe ser: {", ".join(STATUS_COLABORADOR)}'}
            collab.status = data['status']
        if 'email' in data:
            if not validate_email(data['email']):
                return {'success': False, 'error': 'Email invalido'}
            existing = Collaborator.query.filter(Collaborator.email == data['email'], Collaborator.id != collaborator_id).first()
            if existing:
                return {'success': False, 'error': 'El email ya esta en uso'}
            collab.email = data['email']
        if 'phone' in data:
            collab.phone = data['phone']
        db.session.commit()
        return {'success': True, 'message': 'Colaborador actualizado exitosamente'}

    @staticmethod
    def delete(collaborator_id):
        collab = Collaborator.query.get(collaborator_id)
        if not collab:
            return {'success': False, 'error': 'Colaborador no encontrado'}
        db.session.delete(collab)
        db.session.commit()
        return {'success': True, 'message': 'Colaborador eliminado exitosamente'}
