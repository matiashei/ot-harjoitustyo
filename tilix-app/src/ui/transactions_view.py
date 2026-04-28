from datetime import datetime
from tkinter import ttk, Label, Button, Frame, Entry, messagebox, Toplevel
import re


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


COLUMNS = ("date", "description", "amount")
HEADERS = ("Date", "Description", "Amount")


class TransactionsView:
    def __init__(self, root, show_accounts_view, show_new_account_view,
                 transaction_service, account_id, account_name):
        self._root = root
        self._show_accounts_view = show_accounts_view
        self._show_new_account_view = show_new_account_view
        self._transaction_service = transaction_service
        self._frame = Frame(self._root)
        self._account_id = account_id
        self._account_name = account_name

    def start(self):
        self._frame = Frame(self._root)

        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)
        self._frame.columnconfigure(2, weight=1)
        self._frame.columnconfigure(3, weight=1)

        default_label = Label(
            self._frame,
            text=f"Transactions for account {self._account_name}",
            font=("Arial", 14, "bold"),
            bg="grey"
        )
        go_back_button = Button(self._frame, text="⏎ Accounts",
                                bg="lightgreen",
                                command=self._show_accounts_view)

        self._date_text = Label(self._frame, text="Date (YYYY-MM-DD):")
        self._description_text = Label(self._frame, text="Description:")
        self._amount_text = Label(self._frame, text="Amount:")
        self._date_entry = Entry(self._frame)
        self._date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self._description_entry = Entry(self._frame)
        self._amount_entry = Entry(self._frame)
        add_transaction_button = Button(
            self._frame, text="Create transaction", command=self._add_transaction)

        action_frame = Frame(self._frame)
        action_frame.grid(row=1, column=0, columnspan=4,
                          padx=20, pady=(0, 12), sticky="e")

        delete_transaction_button = Button(
            action_frame, text="Delete selected", command=self._delete_transaction)
        edit_transaction_button = Button(
            action_frame, text="Edit selected", command=self._edit_transaction)

        default_label.grid(row=0, column=0, columnspan=3,
                           padx=20, pady=(12, 8), sticky="w")
        go_back_button.grid(row=0, column=3, padx=20, pady=(12, 8), sticky="e")
        edit_transaction_button.pack(side="left", padx=4)
        delete_transaction_button.pack(side="left", padx=4)

        self.tree = ttk.Treeview(self._frame, columns=COLUMNS, show="headings")

        self.tree.tag_configure("evenrow", background="lightyellow")
        self.tree.tag_configure("oddrow", background="white")

        for col, header in zip(COLUMNS, HEADERS):
            self.tree.heading(col, text=header, anchor="w")
            self.tree.column(col, width=300, anchor="w")

        self._get_transactions()
        self.tree.grid(row=2, column=0, columnspan=4,
                       padx=20, pady=10, sticky="nsew")

        self._date_text.grid(row=3, column=0, padx=5, pady=(10, 2), sticky="w")
        self._description_text.grid(
            row=3, column=1, padx=5, pady=(10, 2), sticky="w")
        self._amount_text.grid(row=3, column=2, padx=5,
                               pady=(10, 2), sticky="w")
        self._date_entry.grid(row=4, column=0, padx=5, pady=(0, 10))
        self._description_entry.grid(row=4, column=1, padx=5, pady=(0, 10))
        self._amount_entry.grid(row=4, column=2, padx=5, pady=(0, 10))
        add_transaction_button.grid(row=4, column=3, padx=5, pady=(0, 10))

        self._frame.pack()
        self.tree.bind("<Double-1>", lambda e: self._on_double_click(e))

    def _get_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        transactions = self._transaction_service.find_transactions_by_account_id(
            self._account_id)
        for i, transaction in enumerate(transactions):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", iid=str(transaction.id), values=(
                transaction.date, transaction.description, f"{transaction.amount:.2f} €"), tags=tag)

    def _add_transaction(self):
        date = self._date_entry.get().strip()
        description = self._description_entry.get().strip()
        amount_text = self._amount_entry.get().strip()

        if not date or not description or not amount_text:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if date and not validate_date(date):
            messagebox.showerror(
                "Error", "Must be a valid date in YYYY-MM-DD format")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror(
                "Error", "Amount must be a number, use a dot to separate decimals")
            return

        self._transaction_service.create_transaction(amount, date, description,
                                                     self._account_id)
        self._description_entry.delete(0, "end")
        self._amount_entry.delete(0, "end")
        self._get_transactions()

    def _on_double_click(self, event):
        self._edit_transaction()

    def _delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a transaction to delete it")
            return

        if len(selected) > 1:
            messagebox.showerror(
                "Error", "You can only delete one transaction at a time")
            return

        transaction_id = int(selected[0])
        if messagebox.askyesno("Confirm", "Do you want to delete this transaction?"):
            self._transaction_service.delete_transaction(transaction_id)
            self._get_transactions()

    def _edit_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a transaction to edit it")
            return

        if len(selected) > 1:
            messagebox.showerror(
                "Error", "You can only edit one transaction at a time")
            return

        transaction_id = int(selected[0])
        transaction = self._transaction_service.find_transaction_by_id(
            transaction_id)
        if not transaction:
            messagebox.showerror("Error", "Transaction not found")
            return

        edit_window = Toplevel(self._root)
        edit_window.title("Edit transaction")

        Label(edit_window, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=5,
                                                          pady=5, sticky="w")
        date_entry = Entry(edit_window)
        date_entry.insert(0, transaction.date)
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(edit_window, text="Description").grid(row=1, column=0, padx=5,
                                                    pady=5, sticky="w")
        desc_entry = Entry(edit_window)
        desc_entry.insert(0, transaction.description)
        desc_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(edit_window, text="Amount").grid(row=2, column=0, padx=5,
                                               pady=5, sticky="w")
        amount_entry = Entry(edit_window)
        amount_entry.insert(0, str(transaction.amount))
        amount_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_changes():
            new_date = date_entry.get().strip()
            new_desc = desc_entry.get().strip()
            new_amount_text = amount_entry.get().strip()

            if not new_date or not new_desc or not new_amount_text:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            if new_date and not validate_date(new_date):
                messagebox.showerror(
                    "Error", "Must be a valid date in YYYY-MM-DD format")
                return

            try:
                new_amount = float(new_amount_text)
            except ValueError:
                messagebox.showerror(
                    "Error", "Amount must be a number, use a dot to separate decimals")
                return

            self._transaction_service.update_transaction(
                transaction_id, new_amount, new_date, new_desc)
            edit_window.destroy()
            self._get_transactions()

        save_button = Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=3, column=0, pady=10, sticky="e")
        cancel_button = Button(edit_window, text="Cancel",
                               command=edit_window.destroy)
        cancel_button.grid(row=3, column=1, pady=10, sticky="w")
