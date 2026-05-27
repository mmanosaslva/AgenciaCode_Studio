from app.database.models import Project, Collaborator, Task, CollaboratorProject
from sqlalchemy import func


class ReportController:

    @staticmethod
    def get_projects_summary():
        projects = Project.query.all()
        data = []
        for p in projects:
            total_tasks = p.tasks.count()
            completed_tasks = p.tasks.filter_by(status='completada').count()
            data.append({
                'id': p.id,
                'project_name': p.name,
                'client_name': p.client.name if p.client else 'N/A',
                'status': p.status,
                'start_date': p.start_date,
                'end_date': p.end_date,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks
            })
        return data

    @staticmethod
    def get_collaborator_workload():
        collaborators = Collaborator.query.all()
        data = []
        for c in collaborators:
            active_projects = CollaboratorProject.query.filter_by(
                collaborator_id=c.id, removed_date=None
            ).count()
            assigned_tasks = c.tasks.filter(Task.status != 'cancelada').count()
            tasks_in_progress = c.tasks.filter_by(status='en_progreso').count()
            data.append({
                'id': c.id,
                'name': c.name,
                'role': c.role,
                'active_projects': active_projects,
                'assigned_tasks': assigned_tasks,
                'tasks_in_progress': tasks_in_progress
            })
        return data

    @staticmethod
    def get_tasks_by_status():
        statuses = ['pendiente', 'en_progreso', 'en_revision', 'completada', 'cancelada']
        data = []
        for status in statuses:
            count = Task.query.filter_by(status=status).count()
            data.append({'status': status, 'count': count})
        return data
