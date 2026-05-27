import re
from datetime import date
from app.models.collaborator import CollaboratorModel
from app.models.project import ProjectModel
from app.utils.constants import MAX_PROYECTOS_ACTIVOS


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_required_fields(data, fields):
    missing = [f for f in fields if not data.get(f)]
    return missing


def validate_project_dates(start_date, end_date):
    if start_date >= end_date:
        return 'La fecha de inicio debe ser anterior a la fecha de fin'
    return None


def validate_task_date(due_date, project_end_date):
    if due_date > project_end_date:
        return 'La fecha de vencimiento no puede ser posterior a la fecha de fin del proyecto'
    return None


def validate_assignment(collaborator_id, project):
    if not CollaboratorModel.can_assign_to_project(collaborator_id):
        return {
            'success': False,
            'error': f'El colaborador ya tiene {MAX_PROYECTOS_ACTIVOS} proyectos activos. No puede asignarse a mas.'
        }
    if project.status in ['finalizado', 'cancelado']:
        return {
            'success': False,
            'error': f'No se puede asignar a un proyecto en estado {project.status}'
        }
    return None


def validate_project_deletion(project):
    if ProjectModel.has_tasks_in_progress(project.id):
        return {
            'success': False,
            'error': 'No se puede eliminar un proyecto con tareas en progreso'
        }
    return None
