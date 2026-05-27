import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database.seed import seed_database
from app.views.login_view import LoginView
from app.views.main_view import MainView

flask_app = create_app()
ctx = flask_app.app_context()
ctx.push()

seed_database()

root = tk.Tk()

def on_login_success(user):
    for widget in root.winfo_children():
        widget.destroy()
    MainView(root, user)

LoginView(root, on_login_success)
root.mainloop()

ctx.pop()
