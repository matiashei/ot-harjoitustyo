import unittest
from src import db
from src.repositories.transaction_repository import TransactionRepository
from src.services.transaction_services import TransactionService


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        db.drop_tables()
        db.initialize_database()
        transaction_repository = TransactionRepository(
            db.get_database_connection())
        self.transaction_service = TransactionService(transaction_repository)

    def test_create_transaction(self):
        transaction = self.transaction_service.create_transaction(
            100, "2024-01-01", "Test transaction", 1)
        self.assertEqual(transaction.amount, 100)
        self.assertEqual(transaction.date, "2024-01-01")
        self.assertEqual(transaction.description, "Test transaction")
        self.assertEqual(transaction.account_id, 1)

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
