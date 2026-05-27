import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.auth_controller import AuthController


class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.controller = AuthController()
        self.setup_ui()

    def setup_ui(self):
        self.root.title('AgenciaCode Studio - Inicio de Sesion')
        self.root.geometry('400x300')
        self.root.resizable(False, False)

        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text='AgenciaCode Studio', font=('Arial', 18, 'bold')).pack(pady=(0, 30))

        ttk.Label(main_frame, text='Usuario:').pack(anchor='w')
        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.pack(fill='x', pady=(0, 10))
        self.username_entry.focus()

        ttk.Label(main_frame, text='Contrasena:').pack(anchor='w')
        self.password_entry = ttk.Entry(main_frame, width=30, show='*')
        self.password_entry.pack(fill='x', pady=(0, 20))

        self.password_entry.bind('<Return>', lambda e: self.login())

        ttk.Button(main_frame, text='Ingresar', command=self.login, width=20).pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        result = self.controller.login(username, password)
        if result['success']:
            self.on_login_success(result['user'])
        else:
            messagebox.showerror('Error de inicio de sesion', result['error'])
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()
