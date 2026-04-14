from tkinter import Label, Entry, Button, Frame
from src.db import get_database_connection
from src.repositories.account_repository import AccountRepository
from src.services.account_services import AccountService


class NewAccountView:
    def __init__(self, root, show_accounts_view, username, user_id):
        self._root = root
        self._show_accounts_view = show_accounts_view
        self._frame = Frame(self._root)
        connection = get_database_connection()
        account_repository = AccountRepository(connection)
        self._account_service = AccountService(account_repository)
        self._username = username
        self._user_id = user_id
        self._status_label = None

    def start(self):
        register_label = Label(self._frame, text="NEW ACCOUNT", font=(
            "Arial", 24, "bold"), bg="lightgreen")
        name_label = Label(self._frame, text="Account name")
        self.name_label = Entry(self._frame)
        balance_label = Label(
            self._frame, text="Initial balance (separate decimals with a dot)")
        self._balance_entry = Entry(self._frame)
        self._status_label = Label(self._frame, text="", fg="red")

        self._create_button = Button(
            self._frame, text="Create account", command=self.create_account)

        register_label.grid(row=0, column=0, columnspan=2, pady=30)
        name_label.grid(row=1, column=0, pady=10)
        self.name_label.grid(row=1, column=1, pady=10)
        balance_label.grid(row=2, column=0, pady=10)
        self._balance_entry.grid(row=2, column=1, pady=10)
        self._status_label.grid(row=3, column=0, columnspan=2)
        self._create_button.grid(row=4, column=0, columnspan=2, pady=10)
        self._frame.pack()

    def destroy(self):
        self._frame.destroy()

    def create_account(self):
        name = self.name_label.get().strip()
        balance_text = self._balance_entry.get().strip()

        if not name:
            self._status_label.config(text="Account name is required")
            return

        if not balance_text:
            self._status_label.config(text="Initial balance is required")
            return

        try:
            balance = float(balance_text)
        except ValueError:
            self._status_label.config(text="Initial balance must be a number")
            return

        self._account_service.create_account(name, balance, self._user_id)
        self._show_accounts_view(self._username, self._user_id)
