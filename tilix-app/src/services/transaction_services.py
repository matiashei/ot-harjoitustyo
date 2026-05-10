from src.repositories.transaction_repository import TransactionRepository


class TransactionService:
    """
    Luokka, jonka avulla päivitetään ja haetaan tilitapahtumia tietokannasta TransactionRepositoryn kautta.

    Attributes:
        transaction_repository: Olio, joka hakee ja päivittää tilitapahtumatietoja tietokannasta.
        account_repository: Olio, joka hakee ja päivittää tilitietoja tietokannasta.
    """

    def __init__(self, transaction_repository, account_repository=None):
        """
        Luokan konstruktori, joka käyttää TransactionRepository-oliota."""

        self._transaction_repository = transaction_repository
        self._account_repository = account_repository

    def create_transaction(self, amount, date, description, from_account_id, to_account_id):
        """
        Luo uuden tilitapahtuman.

        Args:
            amount: Tilitapahtuman summa.
            date: Tilitapahtuman päivämäärä.
            description: Tilitapahtuman kuvaus.
            from_account_id: Tili, jolta raha otetaan (debet).
            to_account_id: Tili, jolle raha menee (kredit).

        Returns:
            Transaction: Uusi tilitapahtuman tiedot sisältävä Transaction-olio.
        """
        transaction = self._transaction_repository.create_transaction(
            amount, date, description, from_account_id, to_account_id)

        self._sync_account_balance(from_account_id)
        self._sync_account_balance(to_account_id)

        return transaction

    def find_transactions_by_account_id(self, account_id):
        """
        Hakee kaikki tilitapahtumat tilin id:n perusteella.

        Args:
            account_id: tilin id, jonka tilitapahtumat haetaan.

        Returns:
            Lista Transaction-olioista, jotka täsmäävät tilin id:n kanssa.
        """
        return self._transaction_repository.find_transactions_by_account_id(account_id)

    def find_transaction_by_id(self, transaction_id):
        """
        Hakee yksittäisen tilitapahtuman id:n perusteella.

        Args:
            transaction_id: haettavan tilitapahtuman id.

        Returns:
            Transaction: Transaction-olio, joka täsmää id:n kanssa.
        """
        return self._transaction_repository.find_transaction_by_id(transaction_id)

    def delete_transaction(self, transaction_id):
        """
        Poistaa tilitapahtuman sen id:n perusteella.

        Args:
            transaction_id: poistettavan tilitapahtuman id.

        Returns:
            None
        """
        from_account_id = None
        to_account_id = None
        if self._account_repository:
            transaction = self._transaction_repository.find_transaction_by_id(
                transaction_id)
            if transaction:
                from_account_id = transaction.from_account_id
                to_account_id = transaction.to_account_id

        self._transaction_repository.delete_transaction(transaction_id)
        if from_account_id is not None:
            self._sync_account_balance(from_account_id)
        if to_account_id is not None:
            self._sync_account_balance(to_account_id)

    def update_transaction(self, transaction_id, amount, date, description):
        """
        Päivittää tilitapahtuman tiedot.

        Args:
            transaction_id: Päivitettävän tilitapahtuman id.
            amount: Uusi summa.
            date: Uusi päivämäärä.
            description: Uusi kuvaus.

        Returns:
            None
        """
        from_account_id = None
        to_account_id = None
        if self._account_repository:
            old_transaction = self._transaction_repository.find_transaction_by_id(
                transaction_id)
            if old_transaction:
                from_account_id = old_transaction.from_account_id
                to_account_id = old_transaction.to_account_id

        self._transaction_repository.update_transaction(
            transaction_id, amount, date, description)

        if from_account_id is not None:
            self._sync_account_balance(from_account_id)
        if to_account_id is not None:
            self._sync_account_balance(to_account_id)

    def _sync_account_balance(self, account_id):
        """
        Päivittää tilien balanssit kun tilitapahtumat muuttuvat.

        Args:
            account_id: Päivitettävän tilin id.

        Returns:
            None
        """
        if self._account_repository:
            account = self._account_repository.find_account_by_id(account_id)

        if account:
            transactions = self._transaction_repository.find_transactions_by_account_id(
                account_id)
            new_balance = 0
            for t in transactions:
                if t.to_account_id == account_id:
                    new_balance += t.amount
                elif t.from_account_id == account_id:
                    new_balance -= t.amount
            self._account_repository.update_account_balance(
                account_id, new_balance)
