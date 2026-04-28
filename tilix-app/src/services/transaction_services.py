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

    def create_transaction(self, amount, date, description, account_id):
        """
        Luo uuden tilitapahtuman.

        Args:
            amount: Tilitapahtuman summa.
            date: Tilitapahtuman päivämäärä.
            description: Tilitapahtuman kuvaus.
            account_id: Tilitapahtuman tilin id.

        Returns:
            Transaction: Uusi tilitapahtuman tiedot sisältävä Transaction-olio.
        """
        transaction = self._transaction_repository.create_transaction(
            amount, date, description, account_id)

        self._sync_account_balance(account_id)

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
        account_id = None
        if self._account_repository:
            transaction = self._transaction_repository.find_transaction_by_id(
                transaction_id)
            if transaction:
                account_id = transaction.account_id

        self._transaction_repository.delete_transaction(transaction_id)
        if account_id is not None:
            self._sync_account_balance(account_id)

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
        account_id = None
        if self._account_repository:
            old_transaction = self._transaction_repository.find_transaction_by_id(
                transaction_id)
            if old_transaction:
                account_id = old_transaction.account_id

        self._transaction_repository.update_transaction(
            transaction_id, amount, date, description)

        if account_id is not None:
            self._sync_account_balance(account_id)

    def _sync_account_balance(self, account_id):
        """
        Päivittää tilin balanssin kun tilitapahtumat muuttuvat.

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
            new_balance = sum(t.amount for t in transactions)
            self._account_repository.update_account_balance(
                account_id, new_balance)
