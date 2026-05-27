from app.database.models import Project


class ProjectModel:

    @staticmethod
    def has_tasks_in_progress(project_id):
        project = Project.query.get(project_id)
        if not project:
            return False
        return project.tasks.filter_by(status='en_progreso').count() > 0
