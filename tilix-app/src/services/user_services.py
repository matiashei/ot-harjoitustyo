from src.entities.user import User
from src.repositories.user_repository import UserRepository
from werkzeug.security import check_password_hash

class UserService:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def create_user(self, username, password):
        user = User(username, password)
        return self._user_repository.create_user(user)

    def find_user_by_username(self, username):
        return self._user_repository.find_user_by_username(username)

    def authenticate(self, username, password):
        user = self.find_user_by_username(username)

        if not user:
            return False

        return check_password_hash(user.password, password)