from app import db
from app.database.models import Client
from app.utils.validators import validate_email, validate_required_fields


class ClientController:

    @staticmethod
    def get_all():
        return Client.query.order_by(Client.name).all()

    @staticmethod
    def get_by_id(client_id):
        return Client.query.get(client_id)

    @staticmethod
    def create(data):
        missing = validate_required_fields(data, ['name'])
        if missing:
            return {'success': False, 'error': f'Campos obligatorios faltantes: {", ".join(missing)}'}
        if Client.query.filter_by(name=data['name']).first():
            return {'success': False, 'error': 'El cliente ya existe'}
        if data.get('email') and not validate_email(data['email']):
            return {'success': False, 'error': 'Email invalido'}
        client = Client(
            name=data['name'],
            sector=data.get('sector'),
            email=data.get('email'),
            phone=data.get('phone'),
            contact_person=data.get('contact_person')
        )
        db.session.add(client)
        db.session.commit()
        return {'success': True, 'message': 'Cliente creado exitosamente', 'client': client}

    @staticmethod
    def update(client_id, data):
        client = Client.query.get(client_id)
        if not client:
            return {'success': False, 'error': 'Cliente no encontrado'}
        if 'name' in data and data['name']:
            existing = Client.query.filter(Client.name == data['name'], Client.id != client_id).first()
            if existing:
                return {'success': False, 'error': 'El nombre ya esta en uso'}
            client.name = data['name']
        if 'sector' in data:
            client.sector = data['sector']
        if 'email' in data:
            if data['email'] and not validate_email(data['email']):
                return {'success': False, 'error': 'Email invalido'}
            client.email = data['email']
        if 'phone' in data:
            client.phone = data['phone']
        if 'contact_person' in data:
            client.contact_person = data['contact_person']
        db.session.commit()
        return {'success': True, 'message': 'Cliente actualizado exitosamente'}

    @staticmethod
    def delete(client_id):
        client = Client.query.get(client_id)
        if not client:
            return {'success': False, 'error': 'Cliente no encontrado'}
        db.session.delete(client)
        db.session.commit()
        return {'success': True, 'message': 'Cliente eliminado exitosamente'}
