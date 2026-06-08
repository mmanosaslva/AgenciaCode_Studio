import logging
from flask import current_app, render_template
from flask_mail import Message
from app import mail

logger = logging.getLogger(__name__)


def _send_email(to, subject, template, **context):
    if not current_app.config.get('MAIL_SERVER'):
        logger.warning(f'Mail not configured, skipping email to {to}')
        return
    msg = Message(subject, recipients=[to])
    msg.html = render_template(template, **context)
    try:
        mail.send(msg)
        logger.info(f'Email sent to {to}: {subject}')
    except Exception as e:
        logger.error(f'Failed to send email to {to}: {e}')


def send_welcome_email(user):
    if not user.email:
        logger.warning(f'User {user.username} has no email, skipping welcome')
        return
    _send_email(
        to=user.email,
        subject='Bienvenido a AgenciaCode Studio',
        template='emails/bienvenida.html',
        nombre=user.name,
        username=user.username,
    )


def send_forgot_password_email(user, token):
    if not user.email:
        logger.warning(f'User {user.username} has no email, skipping password reset')
        return
    from flask import url_for
    reset_url = url_for('web.reset_password', token=token, _external=True)
    _send_email(
        to=user.email,
        subject='Recuperacion de contrasena - AgenciaCode Studio',
        template='emails/recuperacion.html',
        nombre=user.name,
        username=user.username,
        reset_url=reset_url,
    )


def send_assignment_email(colaborador, proyecto):
    if not colaborador.email:
        logger.warning(f'Collaborator {colaborador.name} has no email, skipping assignment notification')
        return
    cliente_nombre = proyecto.client.name if proyecto.client else 'N/A'
    _send_email(
        to=colaborador.email,
        subject='Has sido asignado a un proyecto',
        template='emails/asignacion.html',
        nombre=colaborador.name,
        proyecto_nombre=proyecto.name,
        cliente_nombre=cliente_nombre,
        fecha=proyecto.start_date,
    )


def send_overdue_task_email(colaborador, tarea, proyecto):
    if not colaborador.email:
        logger.warning(f'Collaborator {colaborador.name} has no email, skipping overdue notification')
        return
    _send_email(
        to=colaborador.email,
        subject=f'Tarea vencida: {tarea.title}',
        template='emails/tarea_vencida.html',
        nombre=colaborador.name,
        tarea_titulo=tarea.title,
        proyecto_nombre=proyecto.name,
        fecha_vencimiento=tarea.due_date,
        estado=tarea.status,
    )
