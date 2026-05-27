from app import db
from app.database.models import CollaboratorProject, Collaborator, Project
from app.utils.validators import validate_assignment


class AssignmentController:

    @staticmethod
    def get_all():
        return CollaboratorProject.query.all()

    @staticmethod
    def get_by_project(project_id):
        return CollaboratorProject.query.filter_by(project_id=project_id).all()

    @staticmethod
    def get_by_collaborator(collaborator_id):
        return CollaboratorProject.query.filter_by(collaborator_id=collaborator_id).all()

    @staticmethod
    def get_active_assignments():
        return CollaboratorProject.query.filter_by(removed_date=None).all()

    @staticmethod
    def assign(collaborator_id, project_id):
        collaborator = Collaborator.query.get(collaborator_id)
        if not collaborator:
            return {'success': False, 'error': 'Colaborador no encontrado'}
        project = Project.query.get(project_id)
        if not project:
            return {'success': False, 'error': 'Proyecto no encontrado'}
        existing = CollaboratorProject.query.filter_by(
            collaborator_id=collaborator_id,
            project_id=project_id,
            removed_date=None
        ).first()
        if existing:
            return {'success': False, 'error': 'El colaborador ya esta asignado a este proyecto'}
        validation = validate_assignment(collaborator_id, project)
        if validation:
            return validation
        assignment = CollaboratorProject(
            collaborator_id=collaborator_id,
            project_id=project_id
        )
        db.session.add(assignment)
        db.session.commit()
        return {'success': True, 'message': f'{collaborator.name} asignado al proyecto exitosamente'}

    @staticmethod
    def remove(assignment_id):
        assignment = CollaboratorProject.query.get(assignment_id)
        if not assignment:
            return {'success': False, 'error': 'Asignacion no encontrada'}
        from datetime import date
        assignment.removed_date = date.today()
        db.session.commit()
        return {'success': True, 'message': 'Asignacion eliminada exitosamente'}
