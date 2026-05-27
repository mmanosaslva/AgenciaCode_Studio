import tkinter as tk
from tkinter import ttk
from app.views.client_view import ClientView
from app.views.collaborator_view import CollaboratorView
from app.views.project_view import ProjectView
from app.views.task_view import TaskView
from app.views.assignment_view import AssignmentView
from app.views.report_view import ReportView


class MainView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        self.root.title(f'AgenciaCode Studio - Usuario: {self.user.username}')
        self.root.geometry('1024x768')
        self.root.state('zoomed')

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        modulos_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Modulos', menu=modulos_menu)
        modulos_menu.add_command(label='Clientes', command=self.open_clients)
        modulos_menu.add_command(label='Colaboradores', command=self.open_collaborators)
        modulos_menu.add_command(label='Proyectos', command=self.open_projects)
        modulos_menu.add_command(label='Tareas', command=self.open_tasks)
        modulos_menu.add_command(label='Asignaciones', command=self.open_assignments)
        modulos_menu.add_command(label='Reportes', command=self.open_reports)
        modulos_menu.add_separator()
        modulos_menu.add_command(label='Salir', command=self.root.quit)

        self.content_frame = ttk.Frame(self.root, padding=10)
        self.content_frame.pack(fill='both', expand=True)

        self.show_welcome()

    def show_welcome(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ttk.Label(
            self.content_frame,
            text=f'Bienvenido, {self.user.username}',
            font=('Arial', 24, 'bold')
        ).pack(pady=50)
        ttk.Label(
            self.content_frame,
            text='Seleccione un modulo del menu para comenzar',
            font=('Arial', 14)
        ).pack()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def open_clients(self):
        self.clear_content()
        ClientView(self.content_frame)

    def open_collaborators(self):
        self.clear_content()
        CollaboratorView(self.content_frame)

    def open_projects(self):
        self.clear_content()
        ProjectView(self.content_frame)

    def open_tasks(self):
        self.clear_content()
        TaskView(self.content_frame)

    def open_assignments(self):
        self.clear_content()
        AssignmentView(self.content_frame)

    def open_reports(self):
        self.clear_content()
        ReportView(self.content_frame)
