from tkinter import Tk, ttk
from .login_view import LoginView
from .register_view import RegisterView
from .accounts_view import AccountsView

class UI:
    def __init__(self, root):
        self._root = root

    def start(self):
        self._show_login_view()

    def _show_login_view(self):
        self._clear_view()
        login_view = LoginView(
            self._root,
            self._show_register_view,
            self._show_accounts_view
        )
        login_view.start()

    def _show_register_view(self):
        self._clear_view()
        register_view = RegisterView(self._root, self._show_login_view)
        register_view.start()

    def _show_accounts_view(self, username):
        self._clear_view()
        accounts_view = AccountsView(
            self._root,
            self._show_login_view,
            username
        )
        accounts_view.start()

    def _clear_view(self):
        for child in self._root.winfo_children():
            child.destroy()