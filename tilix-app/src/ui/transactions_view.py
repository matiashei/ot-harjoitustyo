from datetime import datetime
from tkinter import ttk, Label, Button, Frame, Entry, messagebox
import re
from wsgiref import validate

def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

COLUMNS = ("date", "description", "amount")
HEADERS = ("Date", "Description", "Amount")


class TransactionsView:
    def __init__(self, root, show_accounts_view, show_new_account_view, transaction_service, account_id, account_name):
        self._root = root
        self._show_accounts_view = show_accounts_view
        self._show_new_account_view = show_new_account_view
        self._transaction_service = transaction_service
        self._frame = Frame(self._root)
        self._account_id = account_id
        self._account_name = account_name

    def start(self):
        self._frame = Frame(self._root)

        default_label = Label(
            self._frame,
            text=f"Transactions for account {self._account_name}",
            font=("Arial", 24, "bold"),
            bg="lightgreen"
        )
        go_back_button = Button(self._frame, text="⏎ Accounts",
                                command=self._show_accounts_view)

        self._date_text = Label(self._frame, text="Date (YYYY-MM-DD)")
        self._description_text = Label(self._frame, text="Description")
        self._amount_text = Label(self._frame, text="Amount")
        self._date_entry = Entry(self._frame)
        self._date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self._description_entry = Entry(self._frame)
        self._amount_entry = Entry(self._frame)
        add_transaction_button = Button(
            self._frame, text="Add transaction", command=self._add_transaction)

        default_label.grid(row=0, column=0, columnspan=2, pady=30)
        go_back_button.grid(row=0, column=2, padx=10, pady=30)

        self.tree = ttk.Treeview(self._frame, columns=COLUMNS, show="headings")

        self.tree.tag_configure("evenrow", background="lightyellow")
        self.tree.tag_configure("oddrow", background="white")

        for col, header in zip(COLUMNS, HEADERS):
            self.tree.heading(col, text=header, anchor="w")
            self.tree.column(col, width=300, anchor="w")

        self._get_transactions()
        self.tree.grid(row=3, column=0, columnspan=4, pady=10)

        self._date_text.grid(row=4, column=0, padx=5, pady=(10, 2), sticky="w")
        self._description_text.grid(row=4, column=1, padx=5, pady=(10, 2), sticky="w")
        self._amount_text.grid(row=4, column=2, padx=5, pady=(10, 2), sticky="w")
        self._date_entry.grid(row=5, column=0, padx=5, pady=(0, 10))
        self._description_entry.grid(row=5, column=1, padx=5, pady=(0, 10))
        self._amount_entry.grid(row=5, column=2, padx=5, pady=(0, 10))
        add_transaction_button.grid(row=5, column=3, padx=5, pady=(0, 10))

        self._frame.pack()

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
            messagebox.showerror("Error", "Must be a valid date in YYYY-MM-DD format")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        self._transaction_service.create_transaction(
            amount, date, description, self._account_id)
        self._description_entry.delete(0, "end")
        self._amount_entry.delete(0, "end")
        self._get_transactions()
