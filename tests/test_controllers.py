import pytest
import datetime
from app import db
from app.database.models import Client, Collaborator


class TestClientController:

    def test_create_client_success(self, app, client_controller):
        with app.app_context():
            result = client_controller.create({
                'name': 'New Client',
                'sector': 'Tech',
                'email': 'new@client.com'
            })
            assert result['success'] is True

    def test_create_client_duplicate_name(self, app, client_controller):
        with app.app_context():
            result = client_controller.create({
                'name': 'Test Corp',
                'sector': 'Tech'
            })
            assert result['success'] is False

    def test_create_client_missing_name(self, app, client_controller):
        with app.app_context():
            result = client_controller.create({'sector': 'Tech'})
            assert result['success'] is False

    def test_get_all_clients(self, app, client_controller):
        with app.app_context():
            clients = client_controller.get_all()
            assert len(clients) >= 1

    def test_get_client_by_id(self, app, client_controller):
        with app.app_context():
            client = client_controller.get_by_id(1)
            assert client is not None
            assert client.name == 'Test Corp'

    def test_update_client(self, app, client_controller):
        with app.app_context():
            result = client_controller.update(1, {'name': 'Test Corp Updated'})
            assert result['success'] is True

    def test_delete_client(self, app, client_controller):
        with app.app_context():
            new_client = Client(name='Temp Client', sector='Temp')
            db.session.add(new_client)
            db.session.commit()

            result = client_controller.delete(new_client.id)
            assert result['success'] is True


class TestCollaboratorController:

    def test_create_collaborator_success(self, app, collaborator_controller):
        with app.app_context():
            result = collaborator_controller.create({
                'name': 'New Collab',
                'role': 'desarrollador',
                'email': 'new.collab@example.com'
            })
            assert result['success'] is True

    def test_create_collaborator_invalid_role(self, app, collaborator_controller):
        with app.app_context():
            result = collaborator_controller.create({
                'name': 'Invalid Role',
                'role': 'hacker',
                'email': 'invalid@example.com'
            })
            assert result['success'] is False

    def test_create_collaborator_duplicate_email(self, app, collaborator_controller):
        with app.app_context():
            result = collaborator_controller.create({
                'name': 'Duplicate Email',
                'role': 'desarrollador',
                'email': 'juan.test@example.com'
            })
            assert result['success'] is False

    def test_get_all_collaborators(self, app, collaborator_controller):
        with app.app_context():
            collabs = collaborator_controller.get_all()
            assert len(collabs) >= 3


class TestProjectController:

    def test_create_project_success(self, app, project_controller):
        with app.app_context():
            result = project_controller.create({
                'name': 'New Project',
                'client_id': 1,
                'start_date': datetime.date(2026, 1, 1),
                'end_date': datetime.date(2026, 12, 31)
            })
            assert result['success'] is True

    def test_create_project_invalid_dates(self, app, project_controller):
        with app.app_context():
            result = project_controller.create({
                'name': 'Bad Dates',
                'client_id': 1,
                'start_date': datetime.date(2026, 12, 31),
                'end_date': datetime.date(2026, 1, 1)
            })
            assert result['success'] is False

    def test_get_all_projects(self, app, project_controller):
        with app.app_context():
            projects = project_controller.get_all()
            assert len(projects) >= 6


class TestTaskController:

    def test_create_task_success(self, app, task_controller):
        with app.app_context():
            result = task_controller.create({
                'project_id': 1,
                'title': 'Test Task',
                'due_date': datetime.date(2026, 6, 30)
            })
            assert result['success'] is True

    def test_create_task_missing_title(self, app, task_controller):
        with app.app_context():
            result = task_controller.create({
                'project_id': 1,
                'due_date': datetime.date(2026, 6, 30)
            })
            assert result['success'] is False

    def test_get_tasks_by_project(self, app, task_controller):
        with app.app_context():
            tasks = task_controller.get_by_project(1)
            assert len(tasks) >= 1


class TestAuthController:

    def test_login_missing_credentials(self, app, auth_controller):
        result = auth_controller.login('', '')
        assert result['success'] is False

    def test_login_invalid_credentials(self, app, auth_controller):
        result = auth_controller.login('nonexistent', 'wrong')
        assert result['success'] is False
