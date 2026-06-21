import pytest
import datetime
from app import db
from app.database.models import User, Client, Collaborator, Project, Task, CollaboratorProject


def _login_admin(client):
    return client.post('/login', data={
        'identificador': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)


def _setup_admin(app):
    from app import bcrypt
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                role='admin',
                name='Admin',
                email='admin@blackbox.com'
            )
            db.session.add(admin)
            db.session.commit()


class TestLoginBlackbox:

    def test_login_page_renders(self, app, client):
        response = client.get('/login')
        assert response.status_code == 200
        assert b'AgenciaCode' in response.data

    def test_login_empty_fields(self, app, client):
        response = client.post('/login', data={
            'identificador': '',
            'password': ''
        }, follow_redirects=True)
        assert b'obligatorios' in response.data

    def test_login_valid_credentials_redirects_to_dashboard(self, app, client):
        _setup_admin(app)
        response = client.post('/login', data={
            'identificador': 'admin',
            'password': 'admin123'
        })
        assert response.status_code == 302
        assert '/dashboard' in response.headers.get('Location', '')

    def test_login_case_insensitive_username(self, app, client):
        _setup_admin(app)
        response = client.post('/login', data={
            'identificador': 'ADMIN',
            'password': 'admin123'
        }, follow_redirects=True)
        assert b'Dashboard' in response.data or b'dashboard' in response.data


class TestRegisterBlackbox:

    def test_register_page_renders(self, app, client):
        response = client.get('/register')
        assert response.status_code == 200

    def test_register_all_fields_empty(self, app, client):
        response = client.post('/register', data={
            'nombre': '',
            'username': '',
            'email': '',
            'password': '',
            'confirm_password': ''
        }, follow_redirects=True)
        assert b'obligatorios' in response.data

    def test_register_password_mismatch(self, app, client):
        response = client.post('/register', data={
            'nombre': 'Test User',
            'username': 'testuser',
            'email': 'test@reg.com',
            'password': 'password123',
            'confirm_password': 'different123'
        }, follow_redirects=True)
        assert b'no coinciden' in response.data

    def test_register_short_password(self, app, client):
        response = client.post('/register', data={
            'nombre': 'Test User',
            'username': 'shortpw',
            'email': 'short@reg.com',
            'password': '1234567',
            'confirm_password': '1234567'
        }, follow_redirects=True)
        assert b'8 caracteres' in response.data

    def test_register_invalid_username_chars(self, app, client):
        response = client.post('/register', data={
            'nombre': 'Test User',
            'username': 'user@name!',
            'email': 'invalid@reg.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        assert b'no permitidos' in response.data or b'letras' in response.data

    def test_register_duplicate_username(self, app, client):
        _setup_admin(app)
        response = client.post('/register', data={
            'nombre': 'Another Admin',
            'username': 'admin',
            'email': 'another@reg.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        assert b'ya existe' in response.data

    def test_register_success(self, app, client):
        response = client.post('/register', data={
            'nombre': 'New User',
            'username': 'newuser_bb',
            'email': 'newuser@bb.com',
            'password': 'securepass123',
            'confirm_password': 'securepass123'
        }, follow_redirects=True)
        assert b'Cuenta creada' in response.data


class TestDashboardBlackbox:

    def test_dashboard_requires_auth(self, app, client):
        response = client.get('/dashboard')
        assert response.status_code == 302

    def test_dashboard_admin_shows_counts(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'Dashboard' in response.data


class TestClientesBlackbox:

    def test_create_cliente_missing_name(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/clientes', data={
            'name': '',
            'email': 'test@cli.com',
            'sector': 'Tecnologia',
        }, follow_redirects=True)
        assert b'Nombre' in response.data

    def test_create_cliente_invalid_email(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/clientes', data={
            'name': 'Valid Name',
            'email': 'not-an-email',
            'sector': 'Tecnologia',
        }, follow_redirects=True)
        assert b'Email' in response.data

    def test_create_cliente_invalid_sector(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/clientes', data={
            'name': 'Valid Name',
            'email': 'valid@cli.com',
            'sector': 'Sector Inexistente',
        }, follow_redirects=True)
        assert b'Sector' in response.data

    def test_create_cliente_success(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/clientes', data={
            'name': 'Cliente Blackbox',
            'email': 'blackbox@cli.com',
            'sector': 'Tecnologia',
            'phone': '3001234567',
            'contact_person': 'Contact Person'
        }, follow_redirects=True)
        assert b'exitosamente' in response.data

    def test_update_cliente(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        with app.app_context():
            cli = Client.query.filter_by(name='Test Corp').first()
            cli_id = cli.id
        response = client.post(f'/clientes/{cli_id}', data={
            '_method': 'PUT',
            'name': 'Test Corp Updated',
            'email': 'updated@corp.com',
            'sector': 'Finanzas',
        }, follow_redirects=True)
        assert b'actualizado' in response.data

    def test_delete_cliente_without_projects(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        with app.app_context():
            cli = Client(name='Delete Me', sector='Otro', email='delete@me.com')
            db.session.add(cli)
            db.session.commit()
            cli_id = cli.id
        response = client.post(f'/clientes/{cli_id}', data={
            '_method': 'DELETE'
        }, follow_redirects=True)
        assert b'eliminado' in response.data


class TestProyectosBlackbox:

    def test_create_proyecto_success(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        with app.app_context():
            cli = Client.query.first()
            cli_id = cli.id
        response = client.post('/proyectos', data={
            'name': 'Proyecto Blackbox',
            'client_id': cli_id,
            'start_date': '2026-01-01',
            'end_date': '2026-12-31',
            'description': 'Test description',
            'status': 'planificacion'
        }, follow_redirects=True)
        assert b'exitosamente' in response.data

    def test_create_proyecto_missing_client(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/proyectos', data={
            'name': 'Sin Cliente',
            'client_id': '',
            'start_date': '2026-01-01',
            'end_date': '2026-12-31',
            'status': 'planificacion'
        }, follow_redirects=True)
        assert b'Cliente' in response.data or b'obligator' in response.data

    def test_create_proyecto_end_before_start(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/proyectos', data={
            'name': 'Fechas Mal',
            'client_id': 1,
            'start_date': '2026-12-31',
            'end_date': '2026-01-01',
            'status': 'planificacion'
        }, follow_redirects=True)
        assert b'posterior' in response.data or b'anterior' in response.data


class TestTareasBlackbox:

    def test_create_tarea_success(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        with app.app_context():
            proj = Project.query.filter_by(status='activo').first()
            pid = proj.id
        response = client.post('/tareas', data={
            'project_id': pid,
            'title': 'Tarea Blackbox',
            'description': 'Descripcion de prueba',
            'priority': 'alta',
            'status': 'pendiente',
            'due_date': '2026-06-30'
        }, follow_redirects=True)
        assert b'exitosamente' in response.data

    def test_create_tarea_missing_title(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/tareas', data={
            'project_id': 1,
            'title': '',
            'priority': 'media',
            'status': 'pendiente',
            'due_date': '2026-06-30'
        }, follow_redirects=True)
        assert b'Titulo' in response.data

    def test_update_tarea_status(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        with app.app_context():
            task = Task.query.first()
            task_id = task.id
        response = client.post(f'/tareas/{task_id}', data={
            '_method': 'PUT',
            'title': 'Tarea Actualizada',
            'description': 'Updated',
            'priority': 'alta',
            'status': 'en_progreso',
            'due_date': '2026-06-30',
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            updated = Task.query.get(task_id)
            assert updated.status == 'en_progreso', \
                f'BUG: Task status not updated. Expected en_progreso, got {updated.status}'

    def test_delete_tarea(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        with app.app_context():
            proj = Project.query.filter_by(status='activo').first()
            task = Task(project_id=proj.id, title='Delete Me Task',
                        status='pendiente', due_date=datetime.date(2026, 6, 30))
            db.session.add(task)
            db.session.commit()
            task_id = task.id
        response = client.post(f'/tareas/{task_id}', data={
            '_method': 'DELETE'
        }, follow_redirects=True)
        assert b'eliminada' in response.data


class TestColaboradoresBlackbox:

    def test_create_colaborador_success(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/colaboradores', data={
            'name': 'Colab Blackbox',
            'role': 'desarrollador',
            'email': 'colab@blackbox.com',
            'phone': '3009876543',
            'status': 'activo'
        }, follow_redirects=True)
        assert b'exitosamente' in response.data

    def test_create_colaborador_invalid_role(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/colaboradores', data={
            'name': 'Invalid Role',
            'role': 'superadmin',
            'email': 'invalid@role.com',
            'status': 'activo'
        }, follow_redirects=True)
        assert b'Rol' in response.data


class TestAsignacionesBlackbox:

    def test_assign_collaborator_to_project(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        with app.app_context():
            collab = Collaborator.query.first()
            proj = Project.query.filter_by(status='planificacion').first()
            collab_id = collab.id
            proj_id = proj.id
        response = client.post('/asignaciones', data={
            'collaborator_id': collab_id,
            'project_id': proj_id
        }, follow_redirects=True)
        assert b'exitosamente' in response.data

    def test_assign_missing_collaborator(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.post('/asignaciones', data={
            'collaborator_id': '',
            'project_id': 1
        }, follow_redirects=True)
        assert b'Colaborador' in response.data or b'obligator' in response.data


class TestReportesBlackbox:

    def test_reportes_page_loads(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.get('/reportes')
        assert response.status_code == 200
        assert b'Reporte' in response.data or b'reporte' in response.data


class TestMisTareasBlackbox:

    def test_mis_tareas_requires_auth(self, app, client):
        response = client.get('/mis-tareas')
        assert response.status_code == 302

    def test_mis_tareas_loads_for_user(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.get('/mis-tareas')
        assert response.status_code == 200


class TestForgotPasswordBlackbox:

    def test_forgot_password_page_renders(self, app, client):
        response = client.get('/forgot-password')
        assert response.status_code == 200

    def test_forgot_password_invalid_email(self, app, client):
        response = client.post('/forgot-password', data={
            'email': 'not-valid'
        })
        assert response.status_code == 200
        with client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            flash_messages = [f[1] for f in flashes]
            has_error = any('email valido' in msg.lower() for msg in flash_messages)
            assert has_error, \
                f'BUG: forgot-password template does not show flash messages. Flashes: {flash_messages}'

    def test_forgot_password_valid_email(self, app, client):
        _setup_admin(app)
        response = client.post('/forgot-password', data={
            'email': 'admin@blackbox.com'
        }, follow_redirects=True)
        assert b'Si el correo existe' in response.data

    def test_reset_password_invalid_token(self, app, client):
        response = client.get('/reset-password/fake-token-12345', follow_redirects=True)
        assert b'invalido' in response.data or b'utilizado' in response.data


class TestMethodOverride:

    def test_get_on_post_only_route(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.get('/clientes/1')
        assert response.status_code == 405

    def test_put_without_method_override(self, app, client):
        _setup_admin(app)
        _login_admin(client)
        response = client.put('/clientes/1', data={
            'name': 'Test',
            'email': 'test@test.com',
            'sector': 'Tecnologia'
        })
        assert response.status_code == 405
