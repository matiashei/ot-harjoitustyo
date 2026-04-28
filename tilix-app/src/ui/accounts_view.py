from tkinter import Label, Button, Frame, ttk, messagebox

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

        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)
        self._frame.columnconfigure(2, weight=1)

        default_label = Label(
            self._frame,
            text=f"You are logged in as {self._username}",
            font=("Arial", 14, "bold"),
            bg="grey"
        )
        logout_button = Button(self._frame, text="Log out",
                               bg="salmon",
                               command=self._show_login_view)

        accounts = self._account_service.find_accounts_by_user_id(
            self._user_id)

        default_label.grid(row=0, column=0, columnspan=2,
                           padx=(20, 10), pady=(12, 8), sticky="w")
        logout_button.grid(row=0, column=2, padx=(
            10, 20), pady=(12, 8), sticky="e")

        action_frame = Frame(self._frame)
        action_frame.grid(row=1, column=0, columnspan=3,
                          padx=20, pady=(0, 12), sticky="e")
        new_account_button = Button(
            action_frame, text="Create new account", command=self._show_new_account_view)
        edit_account_button = Button(
            action_frame, text="Edit selected", command=self._edit_account)
        delete_account_button = Button(
            action_frame, text="Delete selected", command=self._delete_account)
        new_account_button.pack(side="left", padx=4)
        edit_account_button.pack(side="left", padx=4)
        delete_account_button.pack(side="left", padx=4)

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
        self.tree.grid(row=2, column=0, columnspan=3,
                       padx=20, pady=10, sticky="nsew")
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
            row=3, column=0, columnspan=3, pady=(10, 0))

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

    def _edit_account(self):
        item_id = self.tree.focus()
        if not item_id:
            return

        account = self._account_service.find_account_by_id(int(item_id))
        if not account:
            return

        from tkinter import Toplevel, Label, Entry, Button
        edit_window = Toplevel(self._root)
        edit_window.title("Edit account")

        Label(edit_window, text="Name").grid(
            row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = Entry(edit_window)
        name_entry.insert(0, account.name)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        def save():
            new_name = name_entry.get().strip()
            if not new_name:
                return
            self._account_service.update_account_name(int(item_id), new_name)
            edit_window.destroy()
            self._refresh_view()

        Button(edit_window, text="Save", command=save).grid(
            row=1, column=0, padx=5, pady=5)
        Button(edit_window, text="Cancel", command=edit_window.destroy).grid(
            row=1, column=1, padx=5, pady=5)

    def _delete_account(self):
        item_id = self.tree.focus()
        if not item_id:
            return
        if messagebox.askyesno("Confirm", "Delete selected account and its transactions?"):
            self._account_service.delete_account(int(item_id))
            self._restart_view()

    def _refresh_view(self):
        self._frame.destroy()
        self.start()

    def destroy(self):
        self._frame.destroy()
