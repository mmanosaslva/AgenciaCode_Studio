import datetime
from app import db, bcrypt
from app.database.models import User, Client, Collaborator, Project, Task, CollaboratorProject


def seed_database():
    if User.query.first() is not None:
        return

    admin = User(username='admin', password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'), role='admin')
    user1 = User(username='usuario1', password_hash=bcrypt.generate_password_hash('user123').decode('utf-8'), role='user')
    db.session.add_all([admin, user1])

    clients = [
        Client(name='TechCorp Solutions', sector='Tecnologia', email='contacto@techcorp.com', phone='555-0101', contact_person='Laura Martinez'),
        Client(name='DesignLab Studio', sector='Diseno', email='info@designlab.com', phone='555-0202', contact_person='Carlos Vega'),
        Client(name='FinanceGroup SA', sector='Finanzas', email='admin@financegroup.com', phone='555-0303', contact_person='Ana Torres'),
        Client(name='HealthFirst Inc', sector='Salud', email='contact@healthfirst.com', phone='555-0404', contact_person='Pedro Lopez'),
        Client(name='EduLearn Platform', sector='Educacion', email='info@edulearn.com', phone='555-0505', contact_person='Sofia Ruiz'),
    ]
    db.session.add_all(clients)
    db.session.flush()

    collaborators = [
        Collaborator(name='Juan Perez', role='desarrollador', status='activo', email='juan.perez@agenciacode.com', phone='555-1001', hire_date=datetime.date(2025, 1, 15)),
        Collaborator(name='Maria Garcia', role='diseniador', status='activo', email='maria.garcia@agenciacode.com', phone='555-1002', hire_date=datetime.date(2025, 2, 1)),
        Collaborator(name='Carlos Lopez', role='analista', status='activo', email='carlos.lopez@agenciacode.com', phone='555-1003', hire_date=datetime.date(2025, 3, 10)),
        Collaborator(name='Ana Rodriguez', role='desarrollador', status='activo', email='ana.rodriguez@agenciacode.com', phone='555-1004', hire_date=datetime.date(2025, 4, 20)),
        Collaborator(name='Luis Fernandez', role='diseniador', status='inactivo', email='luis.fernandez@agenciacode.com', phone='555-1005', hire_date=datetime.date(2025, 5, 5)),
        Collaborator(name='Elena Martinez', role='analista', status='activo', email='elena.martinez@agenciacode.com', phone='555-1006', hire_date=datetime.date(2025, 6, 15)),
        Collaborator(name='Diego Sanchez', role='desarrollador', status='activo', email='diego.sanchez@agenciacode.com', phone='555-1007', hire_date=datetime.date(2025, 7, 1)),
        Collaborator(name='Sofia Torres', role='diseniador', status='activo', email='sofia.torres@agenciacode.com', phone='555-1008', hire_date=datetime.date(2025, 8, 10)),
    ]
    db.session.add_all(collaborators)
    db.session.flush()

    projects = [
        Project(name='Rediseno Web Corporativo', client_id=clients[0].id, status='activo', start_date=datetime.date(2026, 1, 1), end_date=datetime.date(2026, 6, 30), description='Rediseno completo del sitio web corporativo'),
        Project(name='App Movil de Gestion', client_id=clients[0].id, status='activo', start_date=datetime.date(2026, 2, 1), end_date=datetime.date(2026, 8, 31), description='App movil para gestion de inventarios'),
        Project(name='Plataforma E-learning', client_id=clients[4].id, status='activo', start_date=datetime.date(2026, 3, 1), end_date=datetime.date(2026, 9, 30), description='Plataforma de cursos en linea'),
        Project(name='Dashboard Financiero', client_id=clients[2].id, status='planificacion', start_date=datetime.date(2026, 4, 1), end_date=datetime.date(2026, 10, 31), description='Dashboard de indicadores financieros'),
        Project(name='Sistema de Turnos Medicos', client_id=clients[3].id, status='activo', start_date=datetime.date(2026, 1, 15), end_date=datetime.date(2026, 7, 15), description='Sistema de gestion de turnos'),
        Project(name='Branding Corporativo', client_id=clients[1].id, status='finalizado', start_date=datetime.date(2025, 11, 1), end_date=datetime.date(2026, 2, 28), description='Identidad visual'),
        Project(name='ERP Interno', client_id=clients[2].id, status='activo', start_date=datetime.date(2026, 5, 1), end_date=datetime.date(2026, 12, 31), description='Sistema ERP'),
        Project(name='Landing Page', client_id=clients[1].id, status='cancelado', start_date=datetime.date(2026, 1, 1), end_date=datetime.date(2026, 1, 31), description='Landing page'),
    ]
    db.session.add_all(projects)
    db.session.flush()

    assignments = [
        CollaboratorProject(collaborator_id=collaborators[0].id, project_id=projects[0].id, assigned_date=datetime.date(2026, 1, 2)),
        CollaboratorProject(collaborator_id=collaborators[1].id, project_id=projects[0].id, assigned_date=datetime.date(2026, 1, 5)),
        CollaboratorProject(collaborator_id=collaborators[2].id, project_id=projects[0].id, assigned_date=datetime.date(2026, 1, 10)),
        CollaboratorProject(collaborator_id=collaborators[0].id, project_id=projects[1].id, assigned_date=datetime.date(2026, 2, 5)),
        CollaboratorProject(collaborator_id=collaborators[3].id, project_id=projects[1].id, assigned_date=datetime.date(2026, 2, 10)),
        CollaboratorProject(collaborator_id=collaborators[6].id, project_id=projects[1].id, assigned_date=datetime.date(2026, 2, 15)),
        CollaboratorProject(collaborator_id=collaborators[4].id, project_id=projects[2].id, assigned_date=datetime.date(2026, 3, 5)),
        CollaboratorProject(collaborator_id=collaborators[5].id, project_id=projects[2].id, assigned_date=datetime.date(2026, 3, 10)),
        CollaboratorProject(collaborator_id=collaborators[7].id, project_id=projects[2].id, assigned_date=datetime.date(2026, 3, 15)),
    ]
    db.session.add_all(assignments)

    tasks = [
        Task(project_id=projects[0].id, collaborator_id=collaborators[0].id, title='Configurar servidor web', priority='alta', status='completada', due_date=datetime.date(2026, 2, 1)),
        Task(project_id=projects[0].id, collaborator_id=collaborators[0].id, title='Desarrollar componentes frontend', priority='alta', status='en_progreso', due_date=datetime.date(2026, 4, 30)),
        Task(project_id=projects[0].id, collaborator_id=collaborators[1].id, title='Disenar mockups', priority='media', status='completada', due_date=datetime.date(2026, 3, 1)),
        Task(project_id=projects[1].id, collaborator_id=collaborators[0].id, title='API REST de usuarios', priority='critica', status='en_progreso', due_date=datetime.date(2026, 5, 1)),
        Task(project_id=projects[1].id, collaborator_id=collaborators[3].id, title='Base de datos', priority='alta', status='completada', due_date=datetime.date(2026, 4, 1)),
        Task(project_id=projects[2].id, collaborator_id=collaborators[4].id, title='Diseno de interfaz educativa', priority='alta', status='completada', due_date=datetime.date(2026, 4, 15)),
        Task(project_id=projects[4].id, collaborator_id=collaborators[3].id, title='Modulo de registro de pacientes', priority='critica', status='en_progreso', due_date=datetime.date(2026, 4, 15)),
        Task(project_id=projects[4].id, collaborator_id=collaborators[6].id, title='Modulo de agenda', priority='alta', status='en_progreso', due_date=datetime.date(2026, 5, 15)),
        Task(project_id=projects[6].id, collaborator_id=collaborators[2].id, title='Analisis de procesos financieros', priority='alta', status='pendiente', due_date=datetime.date(2026, 6, 15)),
    ]
    db.session.add_all(tasks)
    db.session.commit()
