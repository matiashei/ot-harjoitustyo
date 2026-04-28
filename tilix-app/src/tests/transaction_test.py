import unittest
from src import db
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository
from src.services.transaction_services import TransactionService


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        db.drop_tables()
        db.initialize_database()
        connection = db.get_database_connection()
        account_repository = AccountRepository(connection)
        self._account_repository = account_repository
        transaction_repository = TransactionRepository(connection)
        self.transaction_service = TransactionService(
            transaction_repository,
            account_repository
        )

        self._account_repository.create_account("Test account", 1)

    def test_create_transaction(self):
        transaction = self.transaction_service.create_transaction(
            100, "2024-01-01", "Test transaction", 1)
        self.assertEqual(transaction.amount, 100)
        self.assertEqual(transaction.date, "2024-01-01")
        self.assertEqual(transaction.description, "Test transaction")
        self.assertEqual(transaction.account_id, 1)

        account = self._account_repository.find_account_by_id(1)
        self.assertEqual(account.balance, 100)

    def test_find_transactions_by_account_id(self):
        self.transaction_service.create_transaction(
            100, "2024-01-01", "Test transaction 1", 1)
        self.transaction_service.create_transaction(
            200, "2024-01-02", "Test transaction 2", 1)
        transactions = self.transaction_service.find_transactions_by_account_id(
            1)
        self.assertEqual(len(transactions), 2)

    def test_delete_transaction(self):
        transaction = self.transaction_service.create_transaction(
            100, "2024-01-01", "Test transaction", 1)
        self.transaction_service.delete_transaction(transaction.id)
        found_transaction = self.transaction_service.find_transaction_by_id(
            transaction.id)
        self.assertIsNone(found_transaction)

        account = self._account_repository.find_account_by_id(1)
        self.assertEqual(account.balance, 0)

    def test_update_transaction(self):
        transaction = self.transaction_service.create_transaction(
            100, "2026-04-02", "Test transaction", 1)
        self.transaction_service.update_transaction(
            transaction.id, 200, "2026-04-01", "Updated transaction")
        updated_transaction = self.transaction_service.find_transaction_by_id(
            transaction.id)
        self.assertEqual(updated_transaction.amount, 200)
        self.assertEqual(updated_transaction.date, "2026-04-01")
        self.assertEqual(updated_transaction.description,
                         "Updated transaction")
        self.assertEqual(updated_transaction.account_id, 1)

        account = self._account_repository.find_account_by_id(1)
        self.assertEqual(account.balance, 200)

    def test_update_transaction_resyncs_balance_when_stale(self):
        transaction = self.transaction_service.create_transaction(
            100, "2026-04-02", "Test transaction", 1)

        self.transaction_service.update_transaction(
            transaction.id, 250, "2026-04-03", "Updated transaction")

        account = self._account_repository.find_account_by_id(1)
        self.assertEqual(account.balance, 250)
