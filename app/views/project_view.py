import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from app.controllers.project_controller import ProjectController
from app.controllers.client_controller import ClientController
from app.utils.constants import STATUS_PROYECTO


class ProjectView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProjectController()
        self.client_controller = ClientController()
        self.selected_id = None
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        ttk.Label(self.parent, text='Gestion de Proyectos', font=('Arial', 16, 'bold')).pack(anchor='w', pady=(0, 10))

        form_frame = ttk.LabelFrame(self.parent, text='Datos del Proyecto', padding=10)
        form_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(form_frame, text='Nombre:').grid(row=0, column=0, sticky='w')
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text='Cliente:').grid(row=0, column=2, sticky='w', padx=(15, 0))
        self.client_combo = ttk.Combobox(form_frame, state='readonly', width=27)
        self.client_combo.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text='Estado:').grid(row=1, column=0, sticky='w')
        self.status_combo = ttk.Combobox(form_frame, values=STATUS_PROYECTO, state='readonly', width=27)
        self.status_combo.grid(row=1, column=1, padx=5, pady=2)
        self.status_combo.set('planificacion')

        ttk.Label(form_frame, text='Fecha Inicio:').grid(row=1, column=2, sticky='w', padx=(15, 0))
        self.start_entry = ttk.Entry(form_frame, width=30)
        self.start_entry.grid(row=1, column=3, padx=5, pady=2)
        self.start_entry.insert(0, date.today().isoformat())

        ttk.Label(form_frame, text='Fecha Fin:').grid(row=2, column=0, sticky='w')
        self.end_entry = ttk.Entry(form_frame, width=30)
        self.end_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text='Descripcion:').grid(row=2, column=2, sticky='w', padx=(15, 0))
        self.desc_entry = ttk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=2, column=3, padx=5, pady=2)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        ttk.Button(btn_frame, text='Nuevo', command=self.clear_form, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Guardar', command=self.save, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Actualizar', command=self.update, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Eliminar', command=self.delete, width=12).pack(side='left', padx=2)

        columns = ('ID', 'Nombre', 'Cliente', 'Estado', 'Inicio', 'Fin')
        self.tree = ttk.Treeview(self.parent, columns=columns, height=15, selectmode='browse')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column('#0', width=0, stretch=False)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.load_clients()

    def load_clients(self):
        clients = self.client_controller.get_all()
        self.client_map = {c.name: c.id for c in clients}
        self.client_combo['values'] = list(self.client_map.keys())

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        projects = self.controller.get_all()
        for p in projects:
            client_name = p.client.name if p.client else 'N/A'
            self.tree.insert('', 'end', values=(
                p.id, p.name, client_name, p.status,
                p.start_date.isoformat() if hasattr(p.start_date, 'isoformat') else p.start_date,
                p.end_date.isoformat() if hasattr(p.end_date, 'isoformat') else p.end_date
            ))

    def clear_form(self):
        self.selected_id = None
        self.name_entry.delete(0, tk.END)
        self.client_combo.set('')
        self.status_combo.set('planificacion')
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, date.today().isoformat())
        self.end_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.name_entry.focus()

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0])['values']
        if not values:
            return
        self.selected_id = values[0]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1] or '')
        self.client_combo.set(values[2] or '')
        self.status_combo.set(values[3] or 'planificacion')
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, values[4] or '')
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, values[5] or '')

    def get_form_data(self):
        return {
            'name': self.name_entry.get().strip(),
            'client_id': self.client_map.get(self.client_combo.get()),
            'client_name': self.client_combo.get(),
            'status': self.status_combo.get(),
            'start_date': self.start_entry.get().strip(),
            'end_date': self.end_entry.get().strip(),
            'description': self.desc_entry.get().strip()
        }

    def save(self):
        data = self.get_form_data()
        if not data['client_id']:
            messagebox.showerror('Error', 'Debe seleccionar un cliente')
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
            messagebox.showwarning('Advertencia', 'Seleccione un proyecto para actualizar')
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
            messagebox.showwarning('Advertencia', 'Seleccione un proyecto para eliminar')
            return
        if messagebox.askyesno('Confirmar', 'Esta seguro de eliminar este proyecto? Se eliminaran sus tareas asociadas.'):
            result = self.controller.delete(self.selected_id)
            if result['success']:
                messagebox.showinfo('Exito', result['message'])
                self.load_data()
                self.clear_form()
            else:
                messagebox.showerror('Error', result['error'])
