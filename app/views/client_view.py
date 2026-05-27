import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.client_controller import ClientController


class ClientView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ClientController()
        self.selected_id = None
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        ttk.Label(self.parent, text='Gestion de Clientes', font=('Arial', 16, 'bold')).pack(anchor='w', pady=(0, 10))

        form_frame = ttk.LabelFrame(self.parent, text='Datos del Cliente', padding=10)
        form_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(form_frame, text='Nombre:').grid(row=0, column=0, sticky='w')
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text='Sector:').grid(row=0, column=2, sticky='w', padx=(15, 0))
        self.sector_entry = ttk.Entry(form_frame, width=30)
        self.sector_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text='Email:').grid(row=1, column=0, sticky='w')
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text='Telefono:').grid(row=1, column=2, sticky='w', padx=(15, 0))
        self.phone_entry = ttk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text='Persona de Contacto:').grid(row=2, column=0, sticky='w')
        self.contact_entry = ttk.Entry(form_frame, width=30)
        self.contact_entry.grid(row=2, column=1, padx=5, pady=2)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        ttk.Button(btn_frame, text='Nuevo', command=self.clear_form, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Guardar', command=self.save, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Actualizar', command=self.update, width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text='Eliminar', command=self.delete, width=12).pack(side='left', padx=2)

        columns = ('ID', 'Nombre', 'Sector', 'Email', 'Telefono', 'Contacto')
        self.tree = ttk.Treeview(self.parent, columns=columns, height=15, selectmode='browse')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column('#0', width=0, stretch=False)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        clients = self.controller.get_all()
        for c in clients:
            self.tree.insert('', 'end', values=(c.id, c.name, c.sector, c.email, c.phone, c.contact_person))

    def clear_form(self):
        self.selected_id = None
        self.name_entry.delete(0, tk.END)
        self.sector_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
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
        self.sector_entry.delete(0, tk.END)
        self.sector_entry.insert(0, values[2] or '')
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[3] or '')
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[4] or '')
        self.contact_entry.delete(0, tk.END)
        self.contact_entry.insert(0, values[5] or '')

    def get_form_data(self):
        return {
            'name': self.name_entry.get().strip(),
            'sector': self.sector_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'phone': self.phone_entry.get().strip(),
            'contact_person': self.contact_entry.get().strip()
        }

    def save(self):
        data = self.get_form_data()
        result = self.controller.create(data)
        if result['success']:
            messagebox.showinfo('Exito', result['message'])
            self.load_data()
            self.clear_form()
        else:
            messagebox.showerror('Error', result['error'])

    def update(self):
        if not self.selected_id:
            messagebox.showwarning('Advertencia', 'Seleccione un cliente para actualizar')
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
            messagebox.showwarning('Advertencia', 'Seleccione un cliente para eliminar')
            return
        if messagebox.askyesno('Confirmar', 'Esta seguro de eliminar este cliente?'):
            result = self.controller.delete(self.selected_id)
            if result['success']:
                messagebox.showinfo('Exito', result['message'])
                self.load_data()
                self.clear_form()
            else:
                messagebox.showerror('Error', result['error'])
