import pytest
import datetime
from app import db
from app.database.models import Collaborator, Project, CollaboratorProject


class TestBusinessRules:

    def test_max_three_active_projects(self, app, assignment_controller):
        with app.app_context():
            collab = Collaborator.query.filter_by(email='juan.test@example.com').first()
            active_projects = Project.query.filter_by(status='activo').all()[:3]

            for proj in active_projects:
                result = assignment_controller.assign(collab.id, proj.id)
                assert result['success'] is True

            fourth = Project(name='Cuarto Proyecto', client_id=1, status='activo',
                             start_date=datetime.date(2026, 1, 1), end_date=datetime.date(2026, 12, 31))
            db.session.add(fourth)
            db.session.commit()

            result = assignment_controller.assign(collab.id, fourth.id)
            assert result['success'] is False
            assert '3' in result['error'] or 'maximo' in result['error'].lower()

    def test_assign_to_planification_project_allowed(self, app, assignment_controller):
        with app.app_context():
            collab = Collaborator.query.filter_by(email='maria.test@example.com').first()
            plan_project = Project.query.filter_by(status='planificacion').first()

            result = assignment_controller.assign(collab.id, plan_project.id)
            assert result['success'] is True

    def test_no_tasks_in_finished_projects(self, app, task_controller):
        with app.app_context():
            project = Project.query.filter_by(status='finalizado').first()

            result = task_controller.create({
                'project_id': project.id,
                'title': 'Tarea en finalizado',
                'due_date': datetime.date(2025, 6, 30)
            })
            assert result['success'] is False
            assert 'finalizado' in result['error'].lower()

    def test_no_tasks_in_cancelled_projects(self, app, task_controller):
        with app.app_context():
            project = Project.query.filter_by(status='cancelado').first()

            result = task_controller.create({
                'project_id': project.id,
                'title': 'Tarea en cancelado',
                'due_date': datetime.date(2026, 1, 15)
            })
            assert result['success'] is False
            assert 'cancelado' in result['error'].lower()

    def test_cannot_delete_project_with_tasks_in_progress(self, app, project_controller):
        with app.app_context():
            project = Project.query.filter_by(name='Proyecto Activo 1').first()

            result = project_controller.delete(project.id)
            assert result['success'] is False
            assert 'progreso' in result['error'].lower()

    def test_can_delete_project_without_tasks_in_progress(self, app, project_controller):
        with app.app_context():
            project = Project.query.filter_by(name='Proyecto Planificado').first()

            result = project_controller.delete(project.id)
            assert result['success'] is True

    def test_project_start_before_end(self, app, project_controller):
        with app.app_context():
            result = project_controller.create({
                'name': 'Fechas Invalidas',
                'client_id': 1,
                'start_date': datetime.date(2026, 12, 31),
                'end_date': datetime.date(2026, 1, 1)
            })
            assert result['success'] is False

    def test_task_date_within_project_range(self, app, task_controller):
        with app.app_context():
            project = Project.query.filter_by(name='Proyecto Activo 1').first()

            result = task_controller.create({
                'project_id': project.id,
                'title': 'Tarea fuera de rango',
                'due_date': datetime.date(2027, 1, 1)
            })
            assert result['success'] is False

    def test_duplicate_assignment_prevented(self, app, assignment_controller):
        with app.app_context():
            collab = Collaborator.query.filter_by(email='carlos.test@example.com').first()
            project = Project.query.filter_by(name='Proyecto Planificado').first()

            result1 = assignment_controller.assign(collab.id, project.id)
            assert result1['success'] is True

            result2 = assignment_controller.assign(collab.id, project.id)
            assert result2['success'] is False

    def test_assign_nonexistent_collaborator(self, app, assignment_controller):
        with app.app_context():
            project = Project.query.filter_by(name='Proyecto Planificado').first()
            result = assignment_controller.assign(999, project.id)
            assert result['success'] is False

    def test_assign_nonexistent_project(self, app, assignment_controller):
        with app.app_context():
            collab = Collaborator.query.filter_by(email='carlos.test@example.com').first()
            result = assignment_controller.assign(collab.id, 999)
            assert result['success'] is False
