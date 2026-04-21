from tkinter import Label, Button, Frame, ttk

COLUMNS = ("name", "balance")
HEADERS = ("Name", "Balance")


class AccountsView:
    def __init__(self, root, show_login_view, show_new_account_view,
                 show_transactions_view, account_service, username, user_id):
        self._root = root
        self._show_login_view = show_login_view
        self._show_new_account_view = show_new_account_view
        self._show_transactions_view = show_transactions_view
        self._account_service = account_service
        self._frame = Frame(self._root)
        self._username = username
        self._user_id = user_id

    def start(self):
        self._frame = Frame(self._root)

        default_label = Label(
            self._frame,
            text=f"You are logged in as {self._username}",
            bg="lightgreen"
        )
        logout_button = Button(self._frame, text="Log out",
                               command=self._show_login_view)
        new_account_button = Button(
            self._frame, text="Create new account", command=self._show_new_account_view)

        accounts = self._account_service.find_accounts_by_user_id(
            self._user_id)

        default_label.grid(pady=30)
        logout_button.grid(row=2, column=0, pady=10)
        new_account_button.grid(row=2, column=1, pady=10)

        style = ttk.Style()
        style.configure("Accounts.Treeview")

        self.tree = ttk.Treeview(self._frame, columns=COLUMNS,
                                 show="headings", style="Accounts.Treeview")

        self.tree.tag_configure("evenrow", background="lightyellow")
        self.tree.tag_configure("oddrow", background="white")

        for col, header in zip(COLUMNS, HEADERS):
            self.tree.heading(col, text=header, anchor="w")
            self.tree.column(col, width=300, anchor="w")
        for i, account in enumerate(accounts):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(
                account.name,
                f"{account.balance:.2f} €"),
                iid=account.id,
                tags=tag)
        self.tree.grid(row=3, column=0, columnspan=2, pady=10)
        self.tree.bind(
            "<Double-1>",
            lambda event: self._open_account()
        )

        total_balance = sum(account.balance for account in accounts)
        total_balance_label = Label(
            self._frame,
            text=f"Total balance: {total_balance:.2f} €",
            font=("Arial", 24, "bold"),
            bg="lightgreen" if total_balance >= 0 else "salmon"
        )
        total_balance_label.grid(
            row=4, column=0, columnspan=2, pady=(10, 0))

        self._frame.pack()

    def _open_account(self):
        item_id = self.tree.focus()
        if not item_id:
            return

        item_values = self.tree.item(item_id, "values")
        if not item_values:
            return

        account_name = item_values[0]
        self._show_transactions_view(int(item_id), account_name)

    def destroy(self):
        self._frame.destroy()
