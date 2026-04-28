from src.repositories.account_repository import AccountRepository


class AccountService:
    """
    Luokka, jonka avulla päivitetään ja haetaan tilitietoja tietokannasta AccountRepositoryn avulla.

    Attributes:
        account_repository: AccountRepository-olio, joka toteuttaa tilitietojen hakemisen ja
        päivittämisen tietokannasta.
    """

    def __init__(self, account_repository, transaction_repository=None):
        """Luokan konstruktori, joka käyttää AccountRepository-oliota.

        Args:
            account_repository: AccountRepository
            transaction_repository: TransactionRepository
        """
        self._account_repository = account_repository
        self._transaction_repository = transaction_repository

    def create_account(self, name, user):
        """
        Luo uuden tilin.

        Args:
            user_id: Tilin omistavan käyttäjän id.

        Returns:
            Account: Uusi tilitiedot sisältävä Account-olio,
            jonka balanssiksi on alustettu 0€.
      """
        user_id = user.user_id if hasattr(user, "user_id") else user
        return self._account_repository.create_account(name, user_id)

    def find_account_by_id(self, account_id):
        """
        Hakee yksittäisen tilin id:n perusteella.

        Args:
            account_id: haettavan tilin id.

        Returns:
            Account: Account-olio, joka täsmää id:n kanssa.
        """
        return self._account_repository.find_account_by_id(account_id)

    def find_accounts_by_user_id(self, user):
        """
        Hakee kaikki käyttäjälle kuuluvat tilit ja niiden tiedot käyttäjän id:n perusteella.

        Args:
            user_id: käyttäjän id, jonka tilit haetaan.

        Returns:
            Lista Account-olioista, jotka täsmäävät id:n kanssa.
        """
        user_id = user.user_id if hasattr(user, "user_id") else user
        return self._account_repository.find_accounts_by_user_id(user_id)

    def delete_account(self, account_id):
        """
        Poistaa tilin id:n perusteella.

        Args:
            account_id: poistettavan tilin id.

        Returns:
            None
        """
        if self._transaction_repository:
            self._transaction_repository.delete_transactions_by_account_id(
                account_id)
        self._account_repository.delete_account(account_id)

    def update_account_name(self, account_id, new_name):
        """
        Päivittää tilin nimen.

        Args:
            account_id: Päivitettävän tilin id.
            new_name: Uusi nimi.

        Returns:
            None
        """
        self._account_repository.update_account_name(account_id, new_name)

    def update_account_balance(self, account_id, new_balance):
        """
        Päivittää tilin balanssin.

        Args:
            account_id: Päivitettävän tilin id.
            new_balance: Uusi balanssi.

        Returns:
            None
        """
        self._account_repository.update_account_balance(
            account_id, new_balance)
