import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from app.controllers.task_controller import TaskController
from app.controllers.project_controller import ProjectController
from app.controllers.collaborator_controller import CollaboratorController
from app.utils.constants import PRIORIDAD_TAREA, STATUS_TAREA


class TaskView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = TaskController()
        self.project_controller = ProjectController()
        self.collab_controller = CollaboratorController()
        self.selected_id = None
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        ttk.Label(self.parent, text='Gestion de Tareas', font=('Arial', 16, 'bold')).pack(anchor='w', pady=(0, 10))

        form_frame = ttk.LabelFrame(self.parent, text='Datos de la Tarea', padding=10)
        form_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(form_frame, text='Titulo:').grid(row=0, column=0, sticky='w')
        self.title_entry = ttk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text='Proyecto:').grid(row=0, column=2, sticky='w', padx=(15, 0))
        self.project_combo = ttk.Combobox(form_frame, state='readonly', width=27)
        self.project_combo.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text='Prioridad:').grid(row=1, column=0, sticky='w')
        self.priority_combo = ttk.Combobox(form_frame, values=PRIORIDAD_TAREA, state='readonly', width=27)
        self.priority_combo.grid(row=1, column=1, padx=5, pady=2)
        self.priority_combo.set('media')

        ttk.Label(form_frame, text='Estado:').grid(row=1, column=2, sticky='w', padx=(15, 0))
        self.status_combo = ttk.Combobox(form_frame, values=STATUS_TAREA, state='readonly', width=27)
        self.status_combo.grid(row=1, column=3, padx=5, pady=2)
        self.status_combo.set('pendiente')

        ttk.Label(form_frame, text='Colaborador:').grid(row=2, column=0, sticky='w')
        self.collab_combo = ttk.Combobox(form_frame, state='readonly', width=27)
        self.collab_combo.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text='Fecha Vencimiento:').grid(row=2, column=2, sticky='w', padx=(15, 0))
        self.due_entry = ttk.Entry(form_frame, width=30)
        self.due_entry.grid(row=2, column=3, padx=5, pady=2)
        self.due_entry.insert(0, date.today().isoformat())

        ttk.Label(form_frame, text='Descripcion:').grid(row=3, column=0, sticky='w')
        self.desc_entry = ttk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=3, column=1, padx=5, pady=2)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=10)
        ttk.Button(btn_frame, text='Nuevo', command=self.clear_form, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Guardar', command=self.save, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Actualizar', command=self.update, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Eliminar', command=self.delete, width=12).pack(side='left', padx=2)

        columns = ('ID', 'Titulo', 'Proyecto', 'Colaborador', 'Prioridad', 'Estado', 'Vencimiento')
        self.tree = ttk.Treeview(self.parent, columns=columns, height=15, selectmode='browse')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)
        self.tree.column('#0', width=0, stretch=False)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.load_projects()
        self.load_collaborators()

    def load_projects(self):
        projects = self.project_controller.get_all()
        self.project_map = {p.name: p.id for p in projects}
        self.project_combo['values'] = list(self.project_map.keys())

    def load_collaborators(self):
        collabs = self.collab_controller.get_all()
        self.collab_map = {c.name: c.id for c in collabs}
        self.collab_combo['values'] = [''] + list(self.collab_map.keys())

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = self.controller.get_all()
        for t in tasks:
            proj_name = t.project.name if t.project else 'N/A'
            collab_name = t.collaborator.name if t.collaborator else ''
            due = t.due_date.isoformat() if hasattr(t.due_date, 'isoformat') else t.due_date
            self.tree.insert('', 'end', values=(t.id, t.title, proj_name, collab_name, t.priority, t.status, due))

    def clear_form(self):
        self.selected_id = None
        self.title_entry.delete(0, tk.END)
        self.project_combo.set('')
        self.priority_combo.set('media')
        self.status_combo.set('pendiente')
        self.collab_combo.set('')
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, date.today().isoformat())
        self.desc_entry.delete(0, tk.END)
        self.title_entry.focus()

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0])['values']
        if not values:
            return
        self.selected_id = values[0]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[1] or '')
        self.project_combo.set(values[2] or '')
        self.collab_combo.set(values[3] or '')
        self.priority_combo.set(values[4] or 'media')
        self.status_combo.set(values[5] or 'pendiente')
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, values[6] or '')

    def get_form_data(self):
        return {
            'title': self.title_entry.get().strip(),
            'project_id': self.project_map.get(self.project_combo.get()),
            'collaborator_id': self.collab_map.get(self.collab_combo.get()),
            'priority': self.priority_combo.get(),
            'status': self.status_combo.get(),
            'due_date': self.due_entry.get().strip(),
            'description': self.desc_entry.get().strip()
        }

    def save(self):
        data = self.get_form_data()
        if not data['project_id']:
            messagebox.showerror('Error', 'Debe seleccionar un proyecto')
            return
        result = self.controller.create(data)
        if result['success']:
            messagebox.showinfo('Exito', result['message'])
            self.load_data()
            self.clear_form()
        else:
            messagebox.showerror('Error', result['error'])

    def update(self):
        if not self.selected_id:
            messagebox.showwarning('Advertencia', 'Seleccione una tarea para actualizar')
            return
        data = self.get_form_data()
        result = self.controller.update(self.selected_id, data)
        if result['success']:
            messagebox.showinfo('Exito', result['message'])
            self.load_data()
            self.clear_form()
        else:
            messagebox.showerror('Error', result['error'])

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning('Advertencia', 'Seleccione una tarea para eliminar')
            return
        if messagebox.askyesno('Confirmar', 'Esta seguro de eliminar esta tarea?'):
            result = self.controller.delete(self.selected_id)
            if result['success']:
                messagebox.showinfo('Exito', result['message'])
                self.load_data()
                self.clear_form()
            else:
                messagebox.showerror('Error', result['error'])
