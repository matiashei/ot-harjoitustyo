class Account:
    def __init__(self, account_id, name, balance, user_id, is_external=False):
        self.id = account_id
        self.name = name
        self.balance = balance
        self.user_id = user_id
        self.is_external = is_external
