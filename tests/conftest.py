import pytest
from app import create_app, db
from app.database.models import (
    User, Client, Collaborator, Project, Task, CollaboratorProject
)
import datetime


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        seed_test_data()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_controller(app):
    from app.controllers.auth_controller import AuthController
    return AuthController()


@pytest.fixture
def project_controller(app):
    from app.controllers.project_controller import ProjectController
    return ProjectController()


@pytest.fixture
def collaborator_controller(app):
    from app.controllers.collaborator_controller import CollaboratorController
    return CollaboratorController()


@pytest.fixture
def task_controller(app):
    from app.controllers.task_controller import TaskController
    return TaskController()


@pytest.fixture
def assignment_controller(app):
    from app.controllers.assignment_controller import AssignmentController
    return AssignmentController()


@pytest.fixture
def client_controller(app):
    from app.controllers.client_controller import ClientController
    return ClientController()


def seed_test_data():
    client = Client(
        name='Test Corp',
        sector='Tech',
        email='test@corp.com',
        phone='555-0000',
        contact_person='Test Person'
    )
    db.session.add(client)
    db.session.flush()

    collaborators = [
        Collaborator(name='Juan Test', role='desarrollador', email='juan.test@example.com'),
        Collaborator(name='Maria Test', role='diseniador', email='maria.test@example.com'),
        Collaborator(name='Carlos Test', role='analista', email='carlos.test@example.com'),
    ]
    db.session.add_all(collaborators)
    db.session.flush()

    projects = [
        Project(name='Proyecto Activo 1', client_id=client.id, status='activo',
                start_date=datetime.date(2026, 1, 1), end_date=datetime.date(2026, 6, 30)),
        Project(name='Proyecto Activo 2', client_id=client.id, status='activo',
                start_date=datetime.date(2026, 2, 1), end_date=datetime.date(2026, 8, 31)),
        Project(name='Proyecto Activo 3', client_id=client.id, status='activo',
                start_date=datetime.date(2026, 3, 1), end_date=datetime.date(2026, 9, 30)),
        Project(name='Proyecto Finalizado', client_id=client.id, status='finalizado',
                start_date=datetime.date(2025, 1, 1), end_date=datetime.date(2025, 12, 31)),
        Project(name='Proyecto Cancelado', client_id=client.id, status='cancelado',
                start_date=datetime.date(2026, 1, 1), end_date=datetime.date(2026, 1, 31)),
        Project(name='Proyecto Planificado', client_id=client.id, status='planificacion',
                start_date=datetime.date(2026, 5, 1), end_date=datetime.date(2026, 12, 31)),
    ]
    db.session.add_all(projects)
    db.session.flush()

    task = Task(
        project_id=projects[0].id,
        collaborator_id=collaborators[0].id,
        title='Tarea en progreso',
        status='en_progreso',
        due_date=datetime.date(2026, 6, 30)
    )
    db.session.add(task)
    db.session.commit()
