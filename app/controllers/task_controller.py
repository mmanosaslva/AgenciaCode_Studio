from app import db
from app.database.models import Task, Project, Collaborator
from app.utils.validators import validate_required_fields, validate_task_date
from app.utils.constants import PRIORIDAD_TAREA, STATUS_TAREA


class TaskController:

    @staticmethod
    def get_all():
        return Task.query.order_by(Task.due_date).all()

    @staticmethod
    def get_by_id(task_id):
        return Task.query.get(task_id)

    @staticmethod
    def get_by_project(project_id):
        return Task.query.filter_by(project_id=project_id).order_by(Task.due_date).all()

    @staticmethod
    def get_by_collaborator(collaborator_id):
        return Task.query.filter_by(collaborator_id=collaborator_id).order_by(Task.due_date).all()

    @staticmethod
    def create(data):
        missing = validate_required_fields(data, ['project_id', 'title', 'due_date'])
        if missing:
            return {'success': False, 'error': f'Campos obligatorios: {", ".join(missing)}'}
        project = Project.query.get(data['project_id'])
        if not project:
            return {'success': False, 'error': 'Proyecto no encontrado'}
        if project.status in ['finalizado', 'cancelado']:
            return {'success': False, 'error': f'No se pueden crear tareas en proyectos {project.status}'}
        if 'priority' in data and data['priority'] and data['priority'] not in PRIORIDAD_TAREA:
            return {'success': False, 'error': f'Prioridad invalida. Debe ser: {", ".join(PRIORIDAD_TAREA)}'}
        error = validate_task_date(data['due_date'], project.end_date)
        if error:
            return {'success': False, 'error': error}
        if 'collaborator_id' in data and data['collaborator_id']:
            collab = Collaborator.query.get(data['collaborator_id'])
            if not collab:
                return {'success': False, 'error': 'Colaborador no encontrado'}
        task = Task(
            project_id=data['project_id'],
            collaborator_id=data.get('collaborator_id'),
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'media'),
            status=data.get('status', 'pendiente'),
            due_date=data['due_date']
        )
        db.session.add(task)
        db.session.commit()
        return {'success': True, 'message': 'Tarea creada exitosamente', 'task': task}

    @staticmethod
    def update(task_id, data):
        task = Task.query.get(task_id)
        if not task:
            return {'success': False, 'error': 'Tarea no encontrada'}
        if 'title' in data and data['title']:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'priority' in data:
            if data['priority'] not in PRIORIDAD_TAREA:
                return {'success': False, 'error': f'Prioridad invalida'}
            task.priority = data['priority']
        if 'status' in data:
            if data['status'] not in STATUS_TAREA:
                return {'success': False, 'error': f'Estado invalido'}
            task.status = data['status']
        if 'due_date' in data:
            project = Project.query.get(task.project_id)
            error = validate_task_date(data['due_date'], project.end_date)
            if error:
                return {'success': False, 'error': error}
            task.due_date = data['due_date']
        if 'collaborator_id' in data:
            if data['collaborator_id']:
                collab = Collaborator.query.get(data['collaborator_id'])
                if not collab:
                    return {'success': False, 'error': 'Colaborador no encontrado'}
            task.collaborator_id = data['collaborator_id']
        db.session.commit()
        return {'success': True, 'message': 'Tarea actualizada exitosamente'}

    @staticmethod
    def delete(task_id):
        task = Task.query.get(task_id)
        if not task:
            return {'success': False, 'error': 'Tarea no encontrada'}
        db.session.delete(task)
        db.session.commit()
        return {'success': True, 'message': 'Tarea eliminada exitosamente'}
