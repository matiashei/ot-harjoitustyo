from tkinter import Label, Button, Frame


class AccountsView:
    def __init__(self, root, show_login_view, show_new_account_view, account_service, username, user_id):
        self._root = root
        self._show_login_view = show_login_view
        self._show_new_account_view = show_new_account_view
        self._account_service = account_service
        self._frame = Frame(self._root)
        self._username = username
        self._user_id = user_id

    def start(self):
        self._frame = Frame(self._root)

        default_label = Label(
            self._frame,
            text=f"You are logged in as {self._username}",
            font=("Arial", 24, "bold"),
            bg="lightgreen"
        )
        logout_button = Button(self._frame, text="Logout",
                               command=self._show_login_view)
        new_account_button = Button(
            self._frame, text="Create new account", command=self._show_new_account_view)

        accounts = self._account_service.find_accounts_by_user_id(
            self._user_id)

        default_label.grid(row=0, column=0, columnspan=2, pady=30)
        logout_button.grid(row=2, column=0, pady=10)
        new_account_button.grid(row=2, column=1, pady=10)

        next_row = 3
        for index, account in enumerate(accounts, start=3):
            account_label = Label(
                self._frame,
                text=f"{account.name}: {account.balance:.2f} €",
                font=("Arial", 16)
            )
            delete_account_button = Button(
                self._frame,
                text="Delete",
                command=lambda account_id=account.id: (
                    self._account_service.delete_account(account_id),
                    self.destroy(),
                    self.start()
                )
            )

            account_label.grid(row=index, column=0,
                               columnspan=2, sticky="w", pady=4)
            delete_account_button.grid(row=index, column=1, sticky="e", pady=4)
            next_row = index + 1

        total_balance = sum(account.balance for account in accounts)
        total_balance_label = Label(
            self._frame,
            text=f"Total balance: {total_balance:.2f} €",
            font=("Arial", 24, "bold"),
            bg="lightgreen" if total_balance >= 0 else "salmon"
        )
        total_balance_label.grid(
            row=next_row, column=0, columnspan=2, pady=(10, 0))

        self._frame.pack()

    def destroy(self):
        self._frame.destroy()
