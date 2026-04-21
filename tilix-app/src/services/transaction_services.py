from src.repositories.transaction_repository import TransactionRepository


class TransactionService:
    def __init__(self, transaction_repository, account_repository=None):
        self._transaction_repository = transaction_repository
        self._account_repository = account_repository

    def create_transaction(self, amount, date, description, account_id):
        transaction = self._transaction_repository.create_transaction(
            amount, date, description, account_id)

        if self._account_repository:
            account = self._account_repository.find_account_by_id(account_id)
            if account:
                self._account_repository.update_account_balance(
                    account_id, account.balance + amount)

        return transaction

    def find_transactions_by_account_id(self, account_id):
        return self._transaction_repository.find_transactions_by_account_id(account_id)

    def find_transaction_by_id(self, transaction_id):
        return self._transaction_repository.find_transaction_by_id(transaction_id)

    def delete_transaction(self, transaction_id):
        self._transaction_repository.delete_transaction(transaction_id)

    def update_transaction(self, transaction_id, amount, date, description):
        self._transaction_repository.update_transaction(
            transaction_id, amount, date, description)
