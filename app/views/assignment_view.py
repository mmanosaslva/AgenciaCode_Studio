import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.assignment_controller import AssignmentController
from app.controllers.project_controller import ProjectController
from app.controllers.collaborator_controller import CollaboratorController


class AssignmentView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = AssignmentController()
        self.project_controller = ProjectController()
        self.collab_controller = CollaboratorController()
        self.selected_id = None
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        ttk.Label(self.parent, text='Gestion de Asignaciones', font=('Arial', 16, 'bold')).pack(anchor='w', pady=(0, 10))

        form_frame = ttk.LabelFrame(self.parent, text='Nueva Asignacion', padding=10)
        form_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(form_frame, text='Colaborador:').grid(row=0, column=0, sticky='w')
        self.collab_combo = ttk.Combobox(form_frame, state='readonly', width=30)
        self.collab_combo.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text='Proyecto:').grid(row=0, column=2, sticky='w', padx=(15, 0))
        self.project_combo = ttk.Combobox(form_frame, state='readonly', width=30)
        self.project_combo.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(form_frame, text='Asignar', command=self.assign, width=12).grid(row=1, column=0, columnspan=4, pady=10)

        columns = ('ID', 'Colaborador', 'Proyecto', 'Fecha Asignacion', 'Fecha Remocion')
        self.tree = ttk.Treeview(self.parent, columns=columns, height=15, selectmode='browse')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.column('#0', width=0, stretch=False)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        ttk.Button(self.parent, text='Remover Asignacion', command=self.remove, width=20).pack(pady=5)

        self.load_combos()

    def load_combos(self):
        collabs = self.collab_controller.get_all()
        self.collab_map = {c.name: c.id for c in collabs}
        self.collab_combo['values'] = list(self.collab_map.keys())

        projects = self.project_controller.get_all()
        self.project_map = {p.name: p.id for p in projects}
        self.project_combo['values'] = list(self.project_map.keys())

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        assignments = self.controller.get_active_assignments()
        for a in assignments:
            collab_name = a.collaborator.name if a.collaborator else 'N/A'
            proj_name = a.project.name if a.project else 'N/A'
            assigned = a.assigned_date.isoformat() if hasattr(a.assigned_date, 'isoformat') else a.assigned_date
            removed = a.removed_date.isoformat() if a.removed_date and hasattr(a.removed_date, 'isoformat') else (a.removed_date or '')
            self.tree.insert('', 'end', values=(a.id, collab_name, proj_name, assigned, removed))

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0])['values']
        if values:
            self.selected_id = values[0]

    def assign(self):
        collab_name = self.collab_combo.get()
        proj_name = self.project_combo.get()
        if not collab_name or not proj_name:
            messagebox.showwarning('Advertencia', 'Debe seleccionar colaborador y proyecto')
            return
        collab_id = self.collab_map.get(collab_name)
        proj_id = self.project_map.get(proj_name)
        result = self.controller.assign(collab_id, proj_id)
        if result['success']:
            messagebox.showinfo('Exito', result['message'])
            self.load_data()
        else:
            messagebox.showerror('Error', result['error'])

    def remove(self):
        if not self.selected_id:
            messagebox.showwarning('Advertencia', 'Seleccione una asignacion para remover')
            return
        if messagebox.askyesno('Confirmar', 'Esta seguro de remover esta asignacion?'):
            result = self.controller.remove(self.selected_id)
            if result['success']:
                messagebox.showinfo('Exito', result['message'])
                self.load_data()
                self.selected_id = None
            else:
                messagebox.showerror('Error', result['error'])
