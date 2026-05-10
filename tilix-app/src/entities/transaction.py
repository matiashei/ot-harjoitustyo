class Transaction:
    def __init__(self, transaction_id, amount, date, description,
                 from_account_id, to_account_id):
        self.id = transaction_id
        self.amount = amount
        self.date = date
        self.description = description
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
