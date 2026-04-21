from src.repositories.account_repository import AccountRepository


class AccountService:
    def __init__(self, account_repository):
        self._account_repository = account_repository

    def create_account(self, name, user):
        user_id = user.user_id if hasattr(user, "user_id") else user
        return self._account_repository.create_account(name, user_id)

    def find_account_by_id(self, account_id):
        return self._account_repository.find_account_by_id(account_id)

    def find_accounts_by_user_id(self, user):
        user_id = user.user_id if hasattr(user, "user_id") else user
        return self._account_repository.find_accounts_by_user_id(user_id)

    def delete_account(self, account_id):
        self._account_repository.delete_account(account_id)

    def update_account_balance(self, account_id, new_balance):
        self._account_repository.update_account_balance(
            account_id, new_balance)
