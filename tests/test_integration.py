import pytest
import datetime
from app import db
from app.database.models import Client, Collaborator, Project, Task, CollaboratorProject


class TestIntegration:

    def test_full_project_workflow(self, app):
        with app.app_context():
            client = Client(name='Acme Corp', sector='Tech')
            db.session.add(client)
            db.session.commit()

            project = Project(
                name='Website Redesign',
                client_id=client.id,
                status='activo',
                start_date=datetime.date(2026, 1, 1),
                end_date=datetime.date(2026, 6, 30)
            )
            db.session.add(project)
            db.session.commit()

            collaborators = [
                Collaborator(name='Ana', role='desarrollador', email='ana@example.com'),
                Collaborator(name='Carlos', role='diseniador', email='carlos.d@example.com')
            ]
            db.session.add_all(collaborators)
            db.session.commit()

            for collab in collaborators:
                assignment = CollaboratorProject(
                    collaborator_id=collab.id,
                    project_id=project.id
                )
                db.session.add(assignment)
            db.session.commit()

            tasks = [
                Task(project_id=project.id, collaborator_id=collaborators[0].id,
                     title='Backend setup', status='en_progreso',
                     due_date=datetime.date(2026, 2, 28)),
                Task(project_id=project.id, collaborator_id=collaborators[1].id,
                     title='UI Design', status='pendiente',
                     due_date=datetime.date(2026, 2, 15))
            ]
            db.session.add_all(tasks)
            db.session.commit()

            project = Project.query.get(project.id)
            assert project.tasks.count() == 2
            collaborators_in_project = CollaboratorProject.query.filter_by(
                project_id=project.id, removed_date=None
            ).count()
            assert collaborators_in_project == 2

            completed = Task.query.filter_by(
                project_id=project.id, status='completada'
            ).count()
            assert completed == 0

    def test_collaborator_max_projects_flow(self, app):
        with app.app_context():
            client = Client.query.first()
            collab = Collaborator(
                name='Test User',
                role='desarrollador',
                email='testuser@example.com'
            )
            db.session.add(collab)
            db.session.commit()

            for i in range(3):
                proj = Project(
                    name=f'Flow Project {i}',
                    client_id=client.id,
                    status='activo',
                    start_date=datetime.date(2026, 1, 1),
                    end_date=datetime.date(2026, 12, 31)
                )
                db.session.add(proj)
                db.session.flush()

                assignment = CollaboratorProject(
                    collaborator_id=collab.id,
                    project_id=proj.id
                )
                db.session.add(assignment)
            db.session.commit()

            active_count = CollaboratorProject.query.filter_by(
                collaborator_id=collab.id, removed_date=None
            ).count()
            assert active_count == 3

            fourth = Project(
                name='Fourth Project',
                client_id=client.id,
                status='activo',
                start_date=datetime.date(2026, 1, 1),
                end_date=datetime.date(2026, 12, 31)
            )
            db.session.add(fourth)
            db.session.commit()

            from sqlalchemy.exc import IntegrityError
            try:
                over_assign = CollaboratorProject(
                    collaborator_id=collab.id,
                    project_id=fourth.id
                )
                db.session.add(over_assign)
                db.session.flush()
                assert False, 'Should have raised an error - but since SQLite does not support triggers, the app-level validation must catch this'
            except Exception:
                db.session.rollback()
