import unittest
from src import db
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository
from src.services.account_services import AccountService
from src.services.transaction_services import TransactionService


class TestAccountService(unittest.TestCase):
    def setUp(self):
        db.drop_tables()
        db.initialize_database()
        connection = db.get_database_connection()
        account_repository = AccountRepository(connection)
        transaction_repository = TransactionRepository(connection)
        self.account_service = AccountService(
            account_repository, transaction_repository)
        self.transaction_service = TransactionService(
            transaction_repository, account_repository)

    def test_create_account(self):
        self.account_service.create_account("Test Account", 1)
        account = self.account_service.find_account_by_id(1)
        self.assertEqual(account.name, "Test Account")
        self.assertEqual(account.balance, 0)
        self.assertEqual(account.user_id, 1)

    def test_find_accounts_by_user_id(self):
        self.account_service.create_account("Test Account 1", 1)
        self.account_service.create_account("Test Account 2", 1)
        accounts = self.account_service.find_accounts_by_user_id(1)
        self.assertEqual(len(accounts), 2)
        self.assertEqual(accounts[0].name, "Test Account 1")
        self.assertEqual(accounts[0].balance, 0)
        self.assertEqual(accounts[0].user_id, 1)
        self.assertEqual(accounts[1].name, "Test Account 2")
        self.assertEqual(accounts[1].balance, 0)
        self.assertEqual(accounts[1].user_id, 1)

    def test_delete_account(self):
        self.account_service.create_account("Test Account", 1)
        self.account_service.delete_account(1)
        account = self.account_service.find_account_by_id(1)
        self.assertIsNone(account)

    def test_update_account_name(self):
        self.account_service.create_account("Account Name", 1)
        self.account_service.update_account_name(1, "New Account Name")
        account = self.account_service.find_account_by_id(1)
        self.assertEqual(account.name, "New Account Name")

    def test_update_account_balance(self):
        self.account_service.create_account("Test Account", 1)
        self.account_service.update_account_balance(1, 2000)
        account = self.account_service.find_account_by_id(1)
        self.assertEqual(account.balance, 2000)
