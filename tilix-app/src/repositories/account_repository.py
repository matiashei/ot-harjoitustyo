from src import db
from src.entities.account import Account


class AccountRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_account(self, name, user_id):
        sql = "INSERT INTO accounts (name, balance, user_id) VALUES (?, 0, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, (name, user_id))
        self._connection.commit()

        account_id = cursor.lastrowid
        return Account(account_id, name, 0, user_id)

    def find_accounts_by_user_id(self, user_id):
        rows = db.query(
            "SELECT * FROM accounts WHERE user_id = ?",
            (user_id,)
        )

        accounts = []
        for row in rows:
            accounts.append(
                Account(row["id"], row["name"], row["balance"], row["user_id"]))

        return accounts

    def find_account_by_id(self, account_id):
        row = db.query_one(
            "SELECT * FROM accounts WHERE id = ?",
            (account_id,)
        )

        if row:
            return Account(row["id"], row["name"], row["balance"], row["user_id"])

        return None

    def delete_account(self, account_id):
        sql = "DELETE FROM accounts WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (account_id,))
        self._connection.commit()

    def update_account_balance(self, account_id, new_balance):
        sql = "UPDATE accounts SET balance = ? WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (new_balance, account_id))
        self._connection.commit()
