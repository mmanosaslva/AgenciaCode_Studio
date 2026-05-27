import tkinter as tk
from tkinter import ttk
from app.controllers.report_controller import ReportController


class ReportView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ReportController()
        self.setup_ui()
        self.load_projects_summary()

    def setup_ui(self):
        ttk.Label(self.parent, text='Reportes', font=('Arial', 16, 'bold')).pack(anchor='w', pady=(0, 10))

        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill='x', pady=(0, 10))
        ttk.Button(btn_frame, text='Resumen de Proyectos', command=self.load_projects_summary, width=25).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Carga de Colaboradores', command=self.load_collaborator_workload, width=25).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Tareas por Estado', command=self.load_tasks_by_status, width=20).pack(side='left', padx=2)

        self.tree_frame = ttk.Frame(self.parent)
        self.tree_frame.pack(fill='both', expand=True)

    def clear_tree(self):
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

    def load_projects_summary(self):
        self.clear_tree()
        columns = ('Proyecto', 'Cliente', 'Estado', 'Inicio', 'Fin', 'Total Tareas', 'Completadas')
        tree = ttk.Treeview(self.tree_frame, columns=columns, height=20, selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.column('#0', width=0, stretch=False)
        tree.pack(fill='both', expand=True)

        data = self.controller.get_projects_summary()
        for item in data:
            tree.insert('', 'end', values=(
                item['project_name'], item['client_name'], item['status'],
                item['start_date'], item['end_date'],
                item['total_tasks'], item['completed_tasks']
            ))

    def load_collaborator_workload(self):
        self.clear_tree()
        columns = ('Nombre', 'Rol', 'Proyectos Activos', 'Tareas Asignadas', 'Tareas en Progreso')
        tree = ttk.Treeview(self.tree_frame, columns=columns, height=20, selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.column('#0', width=0, stretch=False)
        tree.pack(fill='both', expand=True)

        data = self.controller.get_collaborator_workload()
        for item in data:
            tree.insert('', 'end', values=(
                item['name'], item['role'],
                item['active_projects'], item['assigned_tasks'], item['tasks_in_progress']
            ))

    def load_tasks_by_status(self):
        self.clear_tree()
        columns = ('Estado', 'Cantidad')
        tree = ttk.Treeview(self.tree_frame, columns=columns, height=20, selectmode='browse')
        tree.heading('Estado', text='Estado')
        tree.heading('Cantidad', text='Cantidad')
        tree.column('Estado', width=200)
        tree.column('Cantidad', width=150)
        tree.column('#0', width=0, stretch=False)
        tree.pack(fill='both', expand=True)

        data = self.controller.get_tasks_by_status()
        for item in data:
            tree.insert('', 'end', values=(item['status'], item['count']))
