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
        self._account_repository.create_account("Test account 2", 1)
        transaction = self.transaction_service.create_transaction(
            100, "2024-01-01", "Test transaction", 1, 2)
        self.assertEqual(transaction.amount, 100)
        self.assertEqual(transaction.date, "2024-01-01")
        self.assertEqual(transaction.description, "Test transaction")
        self.assertEqual(transaction.from_account_id, 1)
        self.assertEqual(transaction.to_account_id, 2)

        from_account = self._account_repository.find_account_by_id(1)
        to_account = self._account_repository.find_account_by_id(2)
        self.assertEqual(from_account.balance, -100)
        self.assertEqual(to_account.balance, 100)

    def test_find_transactions_by_account_id(self):
        self._account_repository.create_account("Test account 2", 1)
        self._account_repository.create_account("Test account 3", 1)
        self.transaction_service.create_transaction(
          100, "2024-01-01", "Test transaction 1", 1, 2)
        self.transaction_service.create_transaction(
          200, "2024-01-02", "Test transaction 2", 2, 3)
        self.transaction_service.create_transaction(
          50, "2024-01-03", "Test transaction 3", 3, 1)

        account1_transactions = self.transaction_service.find_transactions_by_account_id(1)
        account2_transactions = self.transaction_service.find_transactions_by_account_id(2)
        account3_transactions = self.transaction_service.find_transactions_by_account_id(3)

        self.assertEqual(len(account1_transactions), 2)
        self.assertEqual(len(account2_transactions), 2)
        self.assertEqual(len(account3_transactions), 2)

    def test_delete_transaction(self):
        self._account_repository.create_account("Test account 2", 1)
        transaction = self.transaction_service.create_transaction(
            100, "2024-01-01", "Test transaction", 1, 2)
        self.transaction_service.delete_transaction(transaction.id)
        found_transaction = self.transaction_service.find_transaction_by_id(
            transaction.id)
        self.assertIsNone(found_transaction)

        from_account = self._account_repository.find_account_by_id(1)
        to_account = self._account_repository.find_account_by_id(2)
        self.assertEqual(from_account.balance, 0)
        self.assertEqual(to_account.balance, 0)

    def test_update_transaction(self):
        self._account_repository.create_account("Test account 2", 1)
        transaction = self.transaction_service.create_transaction(
            100, "2026-04-02", "Test transaction", 1, 2)
        self.transaction_service.update_transaction(
            transaction.id, 200, "2026-04-01", "Updated transaction")
        updated_transaction = self.transaction_service.find_transaction_by_id(
            transaction.id)
        self.assertEqual(updated_transaction.amount, 200)
        self.assertEqual(updated_transaction.date, "2026-04-01")
        self.assertEqual(updated_transaction.description,
                         "Updated transaction")
        self.assertEqual(updated_transaction.from_account_id, 1)
        self.assertEqual(updated_transaction.to_account_id, 2)

        from_account = self._account_repository.find_account_by_id(1)
        to_account = self._account_repository.find_account_by_id(2)
        self.assertEqual(from_account.balance, -200)
        self.assertEqual(to_account.balance, 200)

    def test_update_transaction_resyncs_balance_when_stale(self):
        self._account_repository.create_account("Test account 2", 1)
        transaction = self.transaction_service.create_transaction(
            100, "2026-04-02", "Test transaction", 1, 2)

        self.transaction_service.update_transaction(
            transaction.id, 250, "2026-04-03", "Updated transaction")

        from_account = self._account_repository.find_account_by_id(1)
        to_account = self._account_repository.find_account_by_id(2)
        self.assertEqual(from_account.balance, -250)
        self.assertEqual(to_account.balance, 250)
