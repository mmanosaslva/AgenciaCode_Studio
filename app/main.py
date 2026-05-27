import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.database.seed import seed_database
from app.views.login_view import LoginView
from app.views.main_view import MainView


def main():
    app = create_app()

    with app.app_context():
        seed_database()

    root = tk.Tk()

    def on_login_success(user):
        for widget in root.winfo_children():
            widget.destroy()
        MainView(root, user)

    LoginView(root, on_login_success)
    root.mainloop()


if __name__ == '__main__':
    main()
