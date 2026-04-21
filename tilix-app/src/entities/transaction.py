class Transaction:
    def __init__(self, transaction_id, amount, date, description, account_id):
        self.id = transaction_id
        self.amount = amount
        self.date = date
        self.description = description
        self.account_id = account_id
