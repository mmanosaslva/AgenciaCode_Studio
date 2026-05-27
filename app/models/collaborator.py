from app import db
from app.database.models import Collaborator


class CollaboratorModel:

    @staticmethod
    def get_active_projects_count(collaborator_id):
        collab = Collaborator.query.get(collaborator_id)
        if not collab:
            return 0
        return len([p for p in collab.projects if p.status == 'activo'])

    @staticmethod
    def can_assign_to_project(collaborator_id):
        return CollaboratorModel.get_active_projects_count(collaborator_id) < 3
