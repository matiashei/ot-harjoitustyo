from tkinter import Tk, ttk
from src.db import get_database_connection
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository
from src.services.account_services import AccountService
from src.services.transaction_services import TransactionService
from .login_view import LoginView
from .register_view import RegisterView
from .accounts_view import AccountsView
from .new_account_view import NewAccountView


class UI:
    def __init__(self, root):
        self._root = root
        connection = get_database_connection()
        account_repository = AccountRepository(connection)
        transaction_repository = TransactionRepository(connection)
        self._account_service = AccountService(account_repository)
        self._transaction_service = TransactionService(
            transaction_repository, account_repository)

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

    def _show_accounts_view(self, username, user_id):
        self._clear_view()
        accounts_view = AccountsView(
            self._root,
            self._show_login_view,
            lambda: self.show_new_account_view(username, user_id),
            lambda account_id, account_name: self.show_transactions_view(
                account_id, username, user_id, account_name),
            self._account_service,
            username,
            user_id
        )
        accounts_view.start()

    def show_new_account_view(self, username, user_id):
        self._clear_view()
        new_account_view = NewAccountView(
            self._root,
            self._show_accounts_view,
            username,
            user_id
        )
        new_account_view.start()

    def show_transactions_view(self, account_id, username, user_id, account_name):
        from .transactions_view import TransactionsView
        self._clear_view()
        transactions_view = TransactionsView(
            self._root,
            lambda: self._show_accounts_view(username, user_id),
            lambda: self.show_new_account_view(username, user_id),
            self._transaction_service,
            account_id,
            account_name
        )
        transactions_view.start()

    def _clear_view(self):
        for child in self._root.winfo_children():
            child.destroy()
