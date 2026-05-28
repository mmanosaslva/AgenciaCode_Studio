from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import datetime

from app.controllers.auth_controller import AuthController
from app.controllers.client_controller import ClientController
from app.controllers.collaborator_controller import CollaboratorController
from app.controllers.project_controller import ProjectController
from app.controllers.task_controller import TaskController
from app.controllers.assignment_controller import AssignmentController
from app.controllers.report_controller import ReportController

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
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        result = auth_c.login(username, password)
        if result['success']:
            session['user_id'] = result['user'].id
            session['username'] = result['user'].username
            session['role'] = result['user'].role
            return redirect(url_for('web.dashboard'))
        flash(result['error'], 'error')
    return render_template('login.html')


@web_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.login'))


@web_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))


@web_bp.route('/clientes')
@login_required
def clientes():
    clients = client_c.get_all()
    return render_template('clientes.html', clients=clients)


@web_bp.route('/clientes/crear', methods=['POST'])
@login_required
def clientes_crear():
    data = {
        'name': request.form.get('name', '').strip(),
        'sector': request.form.get('sector', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'contact_person': request.form.get('contact_person', '').strip(),
    }
    result = client_c.create(data)
    if result['success']:
        flash('Cliente creado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.clientes'))


@web_bp.route('/clientes/<int:id>/editar', methods=['POST'])
@login_required
def clientes_editar(id):
    data = {
        'name': request.form.get('name', '').strip(),
        'sector': request.form.get('sector', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'contact_person': request.form.get('contact_person', '').strip(),
    }
    result = client_c.update(id, data)
    if result['success']:
        flash('Cliente actualizado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.clientes'))


@web_bp.route('/clientes/<int:id>/eliminar', methods=['POST'])
@login_required
def clientes_eliminar(id):
    result = client_c.delete(id)
    if result['success']:
        flash('Cliente eliminado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.clientes'))


@web_bp.route('/colaboradores')
@login_required
def colaboradores():
    collaborators = collab_c.get_all()
    return render_template('colaboradores.html', collaborators=collaborators)


@web_bp.route('/colaboradores/crear', methods=['POST'])
@login_required
def colaboradores_crear():
    data = {
        'name': request.form.get('name', '').strip(),
        'role': request.form.get('role', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'status': request.form.get('status', 'activo'),
    }
    result = collab_c.create(data)
    if result['success']:
        flash('Colaborador creado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.colaboradores'))


@web_bp.route('/colaboradores/<int:id>/editar', methods=['POST'])
@login_required
def colaboradores_editar(id):
    data = {
        'name': request.form.get('name', '').strip(),
        'role': request.form.get('role', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'status': request.form.get('status', ''),
    }
    result = collab_c.update(id, data)
    if result['success']:
        flash('Colaborador actualizado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.colaboradores'))


@web_bp.route('/colaboradores/<int:id>/eliminar', methods=['POST'])
@login_required
def colaboradores_eliminar(id):
    result = collab_c.delete(id)
    if result['success']:
        flash('Colaborador eliminado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.colaboradores'))


@web_bp.route('/proyectos')
@login_required
def proyectos():
    projects = project_c.get_all()
    clients = client_c.get_all()
    return render_template('proyectos.html', projects=projects, clients=clients)


@web_bp.route('/proyectos/crear', methods=['POST'])
@login_required
def proyectos_crear():
    data = {
        'name': request.form.get('name', '').strip(),
        'client_id': request.form.get('client_id', type=int),
        'status': request.form.get('status', 'planificacion'),
        'start_date': parse_date(request.form.get('start_date')),
        'end_date': parse_date(request.form.get('end_date')),
        'description': request.form.get('description', '').strip(),
    }
    result = project_c.create(data)
    if result['success']:
        flash('Proyecto creado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.proyectos'))


@web_bp.route('/proyectos/<int:id>/editar', methods=['POST'])
@login_required
def proyectos_editar(id):
    data = {
        'name': request.form.get('name', '').strip(),
        'status': request.form.get('status', ''),
        'start_date': parse_date(request.form.get('start_date')),
        'end_date': parse_date(request.form.get('end_date')),
        'description': request.form.get('description', '').strip(),
    }
    result = project_c.update(id, data)
    if result['success']:
        flash('Proyecto actualizado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.proyectos'))


@web_bp.route('/proyectos/<int:id>/eliminar', methods=['POST'])
@login_required
def proyectos_eliminar(id):
    result = project_c.delete(id)
    if result['success']:
        flash('Proyecto eliminado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.proyectos'))


@web_bp.route('/tareas')
@login_required
def tareas():
    tasks = task_c.get_all()
    projects = project_c.get_all()
    collaborators = collab_c.get_all()
    return render_template('tareas.html', tasks=tasks, projects=projects, collaborators=collaborators)


@web_bp.route('/tareas/crear', methods=['POST'])
@login_required
def tareas_crear():
    data = {
        'project_id': request.form.get('project_id', type=int),
        'collaborator_id': request.form.get('collaborator_id', type=int),
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'priority': request.form.get('priority', 'media'),
        'status': request.form.get('status', 'pendiente'),
        'due_date': parse_date(request.form.get('due_date')),
    }
    result = task_c.create(data)
    if result['success']:
        flash('Tarea creada exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.tareas'))


@web_bp.route('/tareas/<int:id>/editar', methods=['POST'])
@login_required
def tareas_editar(id):
    data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'priority': request.form.get('priority', ''),
        'status': request.form.get('status', ''),
        'due_date': parse_date(request.form.get('due_date')),
        'collaborator_id': request.form.get('collaborator_id', type=int),
    }
    result = task_c.update(id, data)
    if result['success']:
        flash('Tarea actualizada exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.tareas'))


@web_bp.route('/tareas/<int:id>/eliminar', methods=['POST'])
@login_required
def tareas_eliminar(id):
    result = task_c.delete(id)
    if result['success']:
        flash('Tarea eliminada exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.tareas'))


@web_bp.route('/asignaciones')
@login_required
def asignaciones():
    assignments = assignment_c.get_active_assignments()
    collaborators = collab_c.get_all()
    projects = project_c.get_all()
    return render_template('asignaciones.html', assignments=assignments, collaborators=collaborators, projects=projects)


@web_bp.route('/asignaciones/crear', methods=['POST'])
@login_required
def asignaciones_crear():
    collaborator_id = request.form.get('collaborator_id', type=int)
    project_id = request.form.get('project_id', type=int)
    result = assignment_c.assign(collaborator_id, project_id)
    if result['success']:
        flash('Asignacion creada exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.asignaciones'))


@web_bp.route('/asignaciones/<int:id>/remover', methods=['POST'])
@login_required
def asignaciones_remover(id):
    result = assignment_c.remove(id)
    if result['success']:
        flash('Asignacion removida exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    return redirect(url_for('web.asignaciones'))


@web_bp.route('/reportes')
@login_required
def reportes():
    projects_summary = report_c.get_projects_summary()
    collab_workload = report_c.get_collaborator_workload()
    tasks_by_status = report_c.get_tasks_by_status()
    return render_template('reportes.html', projects_summary=projects_summary, collab_workload=collab_workload, tasks_by_status=tasks_by_status)
