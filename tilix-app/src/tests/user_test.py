import unittest
from src import db
from src.repositories.user_repository import UserRepository
from src.services.user_services import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        db.drop_tables()
        db.initialize_database()
        user_repository = UserRepository(db.get_database_connection())
        self.user_service = UserService(user_repository)

    def test_create_user(self):
        self.user_service.create_user("testuser", "testpassword")
        user = self.user_service.find_user_by_username("testuser")
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.username, "testuser")

    def test_login_fails_with_wrong_password(self):
        self.user_service.create_user("testuser", "testpassword")
        self.assertFalse(self.user_service.authenticate(
            "testuser", "wrongpassword"))

    def test_login_fails_with_nonexistent_user(self):
        self.user_service.create_user("testuser", "testpassword")
        self.assertFalse(self.user_service.authenticate(
            "wronguser", "testpassword"))

    def test_login_succeeds_with_correct_credentials(self):
        self.user_service.create_user("testuser", "testpassword")
        self.assertTrue(self.user_service.authenticate(
            "testuser", "testpassword"))
