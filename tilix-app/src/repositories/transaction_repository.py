from src import db
from src.entities.transaction import Transaction


class TransactionRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_transaction(self, amount, date, description, account_id):
        sql = "INSERT INTO transactions (amount, date, description, account_id)VALUES (?, ?, ?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, (amount, date, description, account_id))
        self._connection.commit()

        transaction_id = cursor.lastrowid
        return Transaction(transaction_id, amount, date, description, account_id)

    def find_transactions_by_account_id(self, account_id):
        rows = db.query(
            "SELECT * FROM transactions WHERE account_id = ?",
            (account_id,)
        )

        transactions = []
        for row in rows:
            transactions.append(
                Transaction(row["id"], row["amount"], row["date"],
                            row["description"], row["account_id"]))

        return transactions

    def delete_transaction(self, transaction_id):
        sql = "DELETE FROM transactions WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (transaction_id,))
        self._connection.commit()

    def update_transaction(self, transaction_id, amount, date, description):
        sql = "UPDATE transactions SET amount = ?, date = ?, description = ? WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (amount, date, description, transaction_id))
        self._connection.commit()

    def find_transaction_by_id(self, transaction_id):
        row = db.query_one(
            "SELECT * FROM transactions WHERE id = ?",
            (transaction_id,)
        )

        if row:
            return Transaction(row["id"], row["amount"], row["date"],
                               row["description"], row["account_id"])

        return None
