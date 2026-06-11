from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    name = db.Column(db.String(100), default='')
    email = db.Column(db.String(120), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    sector = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(15))
    contact_person = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    projects = db.relationship('Project', back_populates='client', lazy='dynamic')


class Collaborator(db.Model):
    __tablename__ = 'collaborators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='activo')
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    hire_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    projects = db.relationship('Project', secondary='collaborator_project', back_populates='collaborators')
    tasks = db.relationship('Task', back_populates='collaborator', lazy='dynamic')

    def get_active_projects_count(self):
        return len([p for p in self.projects if p.status == 'activo'])

    def can_assign_to_project(self):
        return self.get_active_projects_count() < 3


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    status = db.Column(db.String(20), default='planificacion')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    client = db.relationship('Client', back_populates='projects')
    tasks = db.relationship('Task', back_populates='project', lazy='dynamic')
    collaborators = db.relationship('Collaborator', secondary='collaborator_project', back_populates='projects')


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    collaborator_id = db.Column(db.Integer, db.ForeignKey('collaborators.id'))
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='media')
    status = db.Column(db.String(20), default='pendiente')
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    project = db.relationship('Project', back_populates='tasks')
    collaborator = db.relationship('Collaborator', back_populates='tasks')


class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class CollaboratorProject(db.Model):
    __tablename__ = 'collaborator_project'
    id = db.Column(db.Integer, primary_key=True)
    collaborator_id = db.Column(db.Integer, db.ForeignKey('collaborators.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    assigned_date = db.Column(db.Date, default=db.func.current_date())
    removed_date = db.Column(db.Date)
    collaborator = db.relationship('Collaborator', foreign_keys=[collaborator_id], overlaps="collaborators,projects")
    project = db.relationship('Project', foreign_keys=[project_id], overlaps="collaborators,projects")
