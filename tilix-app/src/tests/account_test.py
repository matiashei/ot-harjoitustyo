import unittest
from src import db
from src.repositories.account_repository import AccountRepository
from src.services.account_services import AccountService


class TestAccountService(unittest.TestCase):
    def setUp(self):
        db.drop_tables()
        db.initialize_database()
        account_repository = AccountRepository(db.get_database_connection())
        self.account_service = AccountService(account_repository)

    def test_create_account(self):
        self.account_service.create_account("Test Account", 1000, 1)
        account = self.account_service.find_account_by_id(1)
        self.assertEqual(account.name, "Test Account")
        self.assertEqual(account.balance, 1000)
        self.assertEqual(account.user_id, 1)

    def test_find_accounts_by_user_id(self):
        self.account_service.create_account("Test Account 1", 1000, 1)
        self.account_service.create_account("Test Account 2", 2000, 1)
        accounts = self.account_service.find_accounts_by_user_id(1)
        self.assertEqual(len(accounts), 2)
        self.assertEqual(accounts[0].name, "Test Account 1")
        self.assertEqual(accounts[0].balance, 1000)
        self.assertEqual(accounts[0].user_id, 1)
        self.assertEqual(accounts[1].name, "Test Account 2")
        self.assertEqual(accounts[1].balance, 2000)
        self.assertEqual(accounts[1].user_id, 1)
