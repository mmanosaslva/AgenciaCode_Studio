import re
import secrets
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps

from app import db, bcrypt
from app.database.models import PasswordResetToken, User, Task
from app.utils.email_service import (
    send_welcome_email,
    send_forgot_password_email,
    send_assignment_email,
    send_overdue_task_email,
)
from app.controllers.auth_controller import AuthController
from app.controllers.client_controller import ClientController
from app.controllers.collaborator_controller import CollaboratorController
from app.controllers.project_controller import ProjectController
from app.controllers.task_controller import TaskController
from app.controllers.assignment_controller import AssignmentController
from app.controllers.report_controller import ReportController

_INVALID_CHARS_RE = re.compile(r'[<>"\'&]')
_USERNAME_RE = re.compile(r'^[a-zA-Z0-9_]+$')
_NAME_RE = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-\.]{3,100}$')
_EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')
_PHONE_RE = re.compile(r'^\+?[0-9]{10,15}$')
_TITLE_RE = re.compile(r'^.{2,200}$')
_SECTORES_VALIDOS = ['Tecnologia', 'Salud', 'Educacion', 'Finanzas',
                     'Retail', 'Manufactura', 'Construccion',
                     'Entretenimiento', 'Consultoria', 'Diseno', 'Otro']
_VALID_ROLES = ['desarrollador', 'diseniador', 'analista']
_VALID_STATUSES = ['activo', 'inactivo']
_VALID_PROJECT_STATUSES = ['activo', 'planificacion', 'finalizado', 'cancelado']
_VALID_PRIORITIES = ['baja', 'media', 'alta', 'critica']
_VALID_TASK_STATUSES = ['pendiente', 'en_progreso', 'en_revision', 'completada', 'cancelada']

web_bp = Blueprint('web', __name__)

auth_c = AuthController()
client_c = ClientController()
collab_c = CollaboratorController()
project_c = ProjectController()
task_c = TaskController()
assignment_c = AssignmentController()
report_c = ReportController()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('web.login'))
        if session.get('role') != 'admin':
            flash('Acceso denegado: se requieren permisos de administrador', 'error')
            return redirect(url_for('web.dashboard'))
        return f(*args, **kwargs)
    return decorated


def parse_date(val):
    if not val:
        return None
    try:
        return datetime.date.fromisoformat(val)
    except (ValueError, TypeError):
        return None


@web_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('web.dashboard'))
    return redirect(url_for('web.login'))


@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identificador = request.form.get('identificador', '').strip().lower()
        password = request.form.get('password', '')
        result = auth_c.login(identificador, password)
        if result['success']:
            session.pop('_flashes', None)
            session.permanent = 'remember' in request.form
            session['user_id'] = result['user'].id
            session['username'] = result['user'].username
            session['role'] = result['user'].role
            return redirect(url_for('web.dashboard'))
        flash(result['error'], 'error')
    return render_template('login.html')


@web_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        if not all([nombre, username, email, password, confirm]):
            flash('Todos los campos son obligatorios', 'error')
            return render_template('register.html')
        if _INVALID_CHARS_RE.search(nombre):
            flash('El nombre contiene caracteres no permitidos', 'error')
            return render_template('register.html')
        if _INVALID_CHARS_RE.search(username):
            flash('El usuario contiene caracteres no permitidos', 'error')
            return render_template('register.html')
        if not _USERNAME_RE.match(username):
            flash('El usuario solo puede contener letras, numeros y guion bajo', 'error')
            return render_template('register.html')
        if _INVALID_CHARS_RE.search(email):
            flash('El email contiene caracteres no permitidos', 'error')
            return render_template('register.html')
        if password != confirm:
            flash('Las contrasenas no coinciden', 'error')
            return render_template('register.html')
        if len(password) < 8:
            flash('La contrasena debe tener al menos 8 caracteres', 'error')
            return render_template('register.html')
        if _INVALID_CHARS_RE.search(password):
            flash('La contrasena contiene caracteres no permitidos', 'error')
            return render_template('register.html')
        result = auth_c.create_user(username, password, role='user', name=nombre, email=email)
        if result['success']:
            flash('Cuenta creada exitosamente. Inicia sesion.', 'success')
            user = User.query.filter_by(username=username).first()
            if user:
                send_welcome_email(user)
            return redirect(url_for('web.login'))
        flash(result['error'], 'error')
    return render_template('register.html')


@web_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.login'))


@web_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email or not _EMAIL_RE.match(email):
            flash('Ingresa un email valido', 'error')
            return render_template('forgot_password.html')
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
            record = PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at)
            db.session.add(record)
            db.session.commit()
            send_forgot_password_email(user, token)
        flash('Si el correo existe, recibiras un enlace de recuperacion', 'success')
        return redirect(url_for('web.login'))
    return render_template('forgot_password.html')


@web_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    record = PasswordResetToken.query.filter_by(token=token, used=False).first()
    if not record:
        flash('Enlace invalido o ya utilizado', 'error')
        return redirect(url_for('web.login'))
    now = datetime.datetime.now(datetime.timezone.utc)
    if record.expires_at.replace(tzinfo=datetime.timezone.utc) < now:
        flash('El enlace ha expirado. Solicita uno nuevo.', 'error')
        return redirect(url_for('web.forgot_password'))
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        if len(password) < 8:
            flash('La contrasena debe tener al menos 8 caracteres', 'error')
            return render_template('reset_password.html', token=token)
        if password != confirm:
            flash('Las contrasenas no coinciden', 'error')
            return render_template('reset_password.html', token=token)
        user = User.query.get(record.user_id)
        if not user:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('web.login'))
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        record.used = True
        db.session.commit()
        flash('Contrasena actualizada exitosamente. Inicia sesion.', 'success')
        return redirect(url_for('web.login'))
    return render_template('reset_password.html', token=token)


@web_bp.route('/dashboard')
@login_required
def dashboard():
    projects = project_c.get_all()
    tasks = task_c.get_all()
    collaborators = collab_c.get_all()
    clients = client_c.get_all()
    projects_count = len([p for p in projects if p.status == 'activo'])
    pending_tasks = len([t for t in tasks if t.status not in ('completada', 'cancelada')])
    collaborators_count = len(collaborators)
    clients_count = len(clients)
    recent_tasks = sorted(
        [t for t in tasks if t.status not in ('completada', 'cancelada')],
        key=lambda t: t.due_date or datetime.date.max
    )[:5]
    return render_template('dashboard.html', username=session.get('username'),
                           projects_count=projects_count, pending_tasks=pending_tasks,
                           collaborators_count=collaborators_count, clients_count=clients_count,
                           recent_tasks=recent_tasks)


# ── CLIENTES ──────────────────────────────────────────────────────────

def _validate_cliente(data):
    errors = []
    name = data.get('name', '')
    if not name or not _NAME_RE.match(name):
        errors.append('Nombre: solo letras, espacios y guiones (3-100 caracteres)')
    email = data.get('email', '')
    if not email or not _EMAIL_RE.match(email.lower()):
        errors.append('Email: formato invalido (ej: correo@dominio.com)')
    sector = data.get('sector', '')
    if sector not in _SECTORES_VALIDOS:
        errors.append('Sector: debe seleccionar un sector valido')
    phone = data.get('phone', '')
    if phone and not _PHONE_RE.match(phone):
        errors.append('Telefono: solo numeros, 10-15 digitos (ej: 3001234567)')
    contact = data.get('contact_person', '')
    if contact and not _NAME_RE.match(contact):
        errors.append('Persona de contacto: solo letras, espacios y guiones (3-100)')
    return errors


@web_bp.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip().lower(),
            'sector': request.form.get('sector', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'contact_person': request.form.get('contact_person', '').strip(),
        }
        errors = _validate_cliente(data)
        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('web.clientes'))
        result = client_c.create(data)
        if result['success']:
            flash('Cliente creado exitosamente', 'success')
        else:
            flash(result['error'], 'error')
        return redirect(url_for('web.clientes'))
    clients = client_c.get_all()
    return render_template('clientes.html', clientes=clients)


@web_bp.route('/clientes/<int:id>', methods=['POST'])
@login_required
def clientes_id(id):
    method = request.form.get('_method', '').upper()
    if method == 'PUT':
        data = {
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'sector': request.form.get('sector', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'contact_person': request.form.get('contact_person', '').strip(),
        }
        errors = _validate_cliente(data)
        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            result = client_c.update(id, data)
            if result['success']:
                flash('Cliente actualizado exitosamente', 'success')
            else:
                flash(result['error'], 'error')
    elif method == 'DELETE':
        result = client_c.delete(id)
        if result['success']:
            flash('Cliente eliminado exitosamente', 'success')
        else:
            flash(result['error'], 'error')
    return redirect(url_for('web.clientes'))


# ── COLABORADORES ─────────────────────────────────────────────────────

def _validate_colaborador(data):
    errors = []
    name = data.get('name', '')
    if not name or not _NAME_RE.match(name):
        errors.append('Nombre: solo letras, espacios y guiones (3-100 caracteres)')
    role = data.get('role', '')
    if role not in _VALID_ROLES:
        errors.append(f'Rol: debe ser uno de: {", ".join(_VALID_ROLES)}')
    status = data.get('status', '')
    if status and status not in _VALID_STATUSES:
        errors.append(f'Estado: debe ser uno de: {", ".join(_VALID_STATUSES)}')
    email = data.get('email', '')
    if not email or not _EMAIL_RE.match(email.lower()):
        errors.append('Email: formato invalido (ej: correo@dominio.com)')
    phone = data.get('phone', '')
    if phone and not _PHONE_RE.match(phone):
        errors.append('Telefono: solo numeros, 10-15 digitos (ej: 3001234567)')
    return errors


@web_bp.route('/colaboradores', methods=['GET', 'POST'])
@login_required
def colaboradores():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', '').strip(),
            'role': request.form.get('role', '').strip(),
            'email': request.form.get('email', '').strip().lower(),
            'phone': request.form.get('phone', '').strip(),
            'status': request.form.get('status', 'activo').strip(),
        }
        errors = _validate_colaborador(data)
        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('web.colaboradores'))
        result = collab_c.create(data)
        if result['success']:
            flash('Colaborador creado exitosamente', 'success')
        else:
            flash(result['error'], 'error')
        return redirect(url_for('web.colaboradores'))
    collaborators = collab_c.get_all()
    return render_template('colaboradores.html', colaboradores=collaborators)


@web_bp.route('/colaboradores/<int:id>', methods=['POST'])
@login_required
def colaboradores_id(id):
    method = request.form.get('_method', '').upper()
    if method == 'PUT':
        data = {
            'name': request.form.get('name', '').strip(),
            'role': request.form.get('role', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'status': request.form.get('status', '').strip(),
        }
        errors = _validate_colaborador(data)
        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            result = collab_c.update(id, data)
            if result['success']:
                flash('Colaborador actualizado exitosamente', 'success')
            else:
                flash(result['error'], 'error')
    elif method == 'DELETE':
        result = collab_c.delete(id)
        if result['success']:
            flash('Colaborador eliminado exitosamente', 'success')
        else:
            flash(result['error'], 'error')
    return redirect(url_for('web.colaboradores'))


# ── PROYECTOS ─────────────────────────────────────────────────────────

def _validate_proyecto(data):
    errors = []
    name = data.get('name', '')
    if not name or len(name) < 2 or len(name) > 150:
        errors.append('Nombre: debe tener entre 2 y 150 caracteres')
    client_id = data.get('client_id')
    if not client_id:
        errors.append('Cliente: obligatorio')
    start = data.get('start_date')
    end = data.get('end_date')
    if not start:
        errors.append('Fecha de inicio: obligatoria')
    if not end:
        errors.append('Fecha de fin: obligatoria')
    if start and end and start >= end:
        errors.append('Fecha de fin debe ser posterior a la fecha de inicio')
    status = data.get('status', '')
    if status and status not in _VALID_PROJECT_STATUSES:
        errors.append(f'Estado: valores validos: {", ".join(_VALID_PROJECT_STATUSES)}')
    return errors


@web_bp.route('/proyectos', methods=['GET', 'POST'])
@login_required
def proyectos():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', '').strip(),
            'client_id': request.form.get('client_id', type=int),
            'start_date': parse_date(request.form.get('start_date')),
            'end_date': parse_date(request.form.get('end_date')),
            'description': request.form.get('description', '').strip(),
            'status': request.form.get('status', 'planificacion').strip(),
        }
        errors = _validate_proyecto(data)
        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('web.proyectos'))
        result = project_c.create(data)
        if result['success']:
            flash('Proyecto creado exitosamente', 'success')
        else:
            flash(result['error'], 'error')
        return redirect(url_for('web.proyectos'))
    projects = project_c.get_all()
    clients = client_c.get_all()
    return render_template('proyectos.html', proyectos=projects, clientes=clients)


@web_bp.route('/proyectos/<int:id>', methods=['POST'])
@login_required
def proyectos_id(id):
    method = request.form.get('_method', '').upper()
    if method == 'PUT':
        data = {
            'name': request.form.get('name', '').strip(),
            'status': request.form.get('status', '').strip(),
            'start_date': parse_date(request.form.get('start_date')),
            'end_date': parse_date(request.form.get('end_date')),
            'description': request.form.get('description', '').strip(),
        }
        errors = _validate_proyecto(data)
        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            result = project_c.update(id, data)
            if result['success']:
                flash('Proyecto actualizado exitosamente', 'success')
            else:
                flash(result['error'], 'error')
    elif method == 'DELETE':
        result = project_c.delete(id)
        if result['success']:
            flash('Proyecto eliminado exitosamente', 'success')
        else:
            flash(result['error'], 'error')
    return redirect(url_for('web.proyectos'))


# ── TAREAS ────────────────────────────────────────────────────────────

def _validate_tarea(data):
    errors = []
    title = data.get('title', '')
    if not title or len(title) < 2 or len(title) > 200:
        errors.append('Titulo: debe tener entre 2 y 200 caracteres')
    elif _INVALID_CHARS_RE.search(title):
        errors.append('Titulo: contiene caracteres no permitidos')
    if not data.get('project_id'):
        errors.append('Proyecto: obligatorio')
    priority = data.get('priority', '')
    if priority and priority not in _VALID_PRIORITIES:
        errors.append(f'Prioridad: valores validos: {", ".join(_VALID_PRIORITIES)}')
    status = data.get('status', '')
    if status and status not in _VALID_TASK_STATUSES:
        errors.append(f'Estado: valores validos: {", ".join(_VALID_TASK_STATUSES)}')
    return errors


@web_bp.route('/tareas', methods=['GET', 'POST'])
@login_required
def tareas():
    if request.method == 'POST':
        data = {
            'project_id': request.form.get('project_id', type=int),
            'collaborator_id': request.form.get('collaborator_id', type=int),
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'priority': request.form.get('priority', 'media').strip(),
            'status': request.form.get('status', 'pendiente').strip(),
            'due_date': parse_date(request.form.get('due_date')),
        }
        errors = _validate_tarea(data)
        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('web.tareas'))
        result = task_c.create(data)
        if result['success']:
            flash('Tarea creada exitosamente', 'success')
        else:
            flash(result['error'], 'error')
        return redirect(url_for('web.tareas'))
    tasks = task_c.get_all()
    projects = project_c.get_all()
    collaborators = collab_c.get_all()
    return render_template('tareas.html', tareas=tasks, proyectos=projects, colaboradores=collaborators)


@web_bp.route('/tareas/<int:id>', methods=['POST'])
@login_required
def tareas_id(id):
    method = request.form.get('_method', '').upper()
    if method == 'PUT':
        data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'priority': request.form.get('priority', '').strip(),
            'status': request.form.get('status', '').strip(),
            'due_date': parse_date(request.form.get('due_date')),
            'collaborator_id': request.form.get('collaborator_id', type=int),
        }
        errors = _validate_tarea(data)
        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            result = task_c.update(id, data)
            if result['success']:
                flash('Tarea actualizada exitosamente', 'success')
            else:
                flash(result['error'], 'error')
    elif method == 'DELETE':
        result = task_c.delete(id)
        if result['success']:
            flash('Tarea eliminada exitosamente', 'success')
        else:
            flash(result['error'], 'error')
    return redirect(url_for('web.tareas'))


# ── ASIGNACIONES ──────────────────────────────────────────────────────

def _validate_asignacion(data):
    errors = []
    if not data.get('collaborator_id'):
        errors.append('Colaborador: obligatorio')
    if not data.get('project_id'):
        errors.append('Proyecto: obligatorio')
    return errors


@web_bp.route('/asignaciones', methods=['GET', 'POST'])
@login_required
def asignaciones():
    if request.method == 'POST':
        collaborator_id = request.form.get('collaborator_id', type=int)
        project_id = request.form.get('project_id', type=int)
        errors = _validate_asignacion({'collaborator_id': collaborator_id, 'project_id': project_id})
        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('web.asignaciones'))
        result = assignment_c.assign(collaborator_id, project_id)
        if result['success']:
            flash('Asignacion creada exitosamente', 'success')
            from app.database.models import Collaborator, Project
            col = Collaborator.query.get(collaborator_id)
            proj = Project.query.get(project_id)
            if col and proj:
                send_assignment_email(col, proj)
        else:
            flash(result['error'], 'error')
        return redirect(url_for('web.asignaciones'))
    assignments = assignment_c.get_active_assignments()
    collaborators = collab_c.get_all()
    projects = project_c.get_all()
    return render_template('asignaciones.html', asignaciones=assignments, colaboradores=collaborators, proyectos=projects)


@web_bp.route('/asignaciones/<int:id>', methods=['POST'])
@login_required
def asignaciones_id(id):
    method = request.form.get('_method', '').upper()
    if method == 'DELETE':
        result = assignment_c.remove(id)
        if result['success']:
            flash('Asignacion removida exitosamente', 'success')
        else:
            flash(result['error'], 'error')
    return redirect(url_for('web.asignaciones'))


# ── REPORTES ──────────────────────────────────────────────────────────

@web_bp.route('/reportes')
@login_required
def reportes():
    projects_summary = report_c.get_projects_summary()
    collab_workload = report_c.get_collaborator_workload()
    tasks_by_status = report_c.get_tasks_by_status()
    tasks_map = {item['status']: item['count'] for item in tasks_by_status}
    stats = {
        'completadas': tasks_map.get('completada', 0),
        'pendientes': tasks_map.get('pendiente', 0),
        'en_progreso': tasks_map.get('en_progreso', 0),
        'eficiencia': 0
    }
    total = stats['completadas'] + stats['pendientes'] + stats['en_progreso']
    if total > 0:
        stats['eficiencia'] = round(stats['completadas'] / total * 100)
    tareas = task_c.get_all()
    return render_template('reportes.html', projects_summary=projects_summary, collab_workload=collab_workload,
                           tasks_by_status=tasks_by_status, stats=stats, tareas=tareas)


@web_bp.route('/admin/check-overdue')
@login_required
@admin_required
def check_overdue():
    today = datetime.date.today()
    overdue_tasks = Task.query.filter(
        Task.due_date < today,
        Task.status.notin_(['completada', 'cancelada']),
        Task.collaborator_id.isnot(None),
    ).all()
    sent_count = 0
    for t in overdue_tasks:
        if t.collaborator and t.project:
            send_overdue_task_email(t.collaborator, t, t.project)
            sent_count += 1
    flash(f'{sent_count} correos de tareas vencidas enviados', 'success')
    return redirect(url_for('web.reportes'))
