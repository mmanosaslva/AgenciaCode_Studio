from app import db
from app.database.models import Project, Client
from app.utils.validators import validate_required_fields, validate_project_dates, validate_project_deletion
from app.utils.constants import STATUS_PROYECTO


class ProjectController:

    @staticmethod
    def get_all():
        return Project.query.order_by(Project.name).all()

    @staticmethod
    def get_by_id(project_id):
        return Project.query.get(project_id)

    @staticmethod
    def get_active():
        return Project.query.filter_by(status='activo').all()

    @staticmethod
    def create(data):
        missing = validate_required_fields(data, ['name', 'client_id', 'start_date', 'end_date'])
        if missing:
            return {'success': False, 'error': f'Campos obligatorios: {", ".join(missing)}'}
        client = Client.query.get(data['client_id'])
        if not client:
            return {'success': False, 'error': 'Cliente no encontrado'}
        error = validate_project_dates(data['start_date'], data['end_date'])
        if error:
            return {'success': False, 'error': error}
        project = Project(
            name=data['name'],
            client_id=data['client_id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            description=data.get('description'),
            status=data.get('status', 'planificacion')
        )
        db.session.add(project)
        db.session.commit()
        return {'success': True, 'message': 'Proyecto creado exitosamente', 'project': project}

    @staticmethod
    def update(project_id, data):
        project = Project.query.get(project_id)
        if not project:
            return {'success': False, 'error': 'Proyecto no encontrado'}
        if 'name' in data and data['name']:
            project.name = data['name']
        if 'status' in data:
            if data['status'] not in STATUS_PROYECTO:
                return {'success': False, 'error': f'Estado invalido. Debe ser: {", ".join(STATUS_PROYECTO)}'}
            project.status = data['status']
        if 'start_date' in data and 'end_date' in data:
            error = validate_project_dates(data['start_date'], data['end_date'])
            if error:
                return {'success': False, 'error': error}
            project.start_date = data['start_date']
            project.end_date = data['end_date']
        elif 'start_date' in data:
            if data['start_date'] >= project.end_date:
                return {'success': False, 'error': 'La fecha de inicio debe ser anterior a la fecha de fin'}
            project.start_date = data['start_date']
        elif 'end_date' in data:
            if project.start_date >= data['end_date']:
                return {'success': False, 'error': 'La fecha de inicio debe ser anterior a la fecha de fin'}
            project.end_date = data['end_date']
        if 'description' in data:
            project.description = data['description']
        db.session.commit()
        return {'success': True, 'message': 'Proyecto actualizado exitosamente'}

    @staticmethod
    def delete(project_id):
        project = Project.query.get(project_id)
        if not project:
            return {'success': False, 'error': 'Proyecto no encontrado'}
        validation = validate_project_deletion(project)
        if validation:
            return validation
        db.session.delete(project)
        db.session.commit()
        return {'success': True, 'message': 'Proyecto eliminado exitosamente'}
