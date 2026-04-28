from src import db
from src.entities.account import Account


class AccountRepository:
    """
    Luokka, jonka avulla voidaan hakea, luoda, päivittää ja poistaa tilitietoja tietokannasta.

    Attributes:
        connection: Tietokantayhteys, joka mahdollistaa SQL-kyselyiden suorittamisen.
    """

    def __init__(self, connection):
        """Luokan konstruktori, joka ottaa tietokantayhteyden."""
        self._connection = connection

    def create_account(self, name, user_id):
        """Luo uuden tilin tietokantaan.

        Args:
            name: Tilin nimi.
            user_id: Tilin omistavan käyttäjän id.

        Returns:
            Account: Uusi tilitiedot sisältävä Account-olio,
            jonka balanssiksi on alustettu 0€.
            """
        sql = "INSERT INTO accounts (name, balance, user_id) VALUES (?, 0, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, (name, user_id))
        self._connection.commit()

        account_id = cursor.lastrowid
        return Account(account_id, name, 0, user_id)

    def find_accounts_by_user_id(self, user_id):
        """Hakee tietokannasta kaikki käyttäjälle kuuluvat tilit ja niiden tiedot.

        Args:
            user_id: käyttäjän id, jonka tilit haetaan.

        Returns:
            Lista Account-olioista, jotka täsmäävät id:n kanssa.
            """
        rows = db.query(
            """
            SELECT
                accounts.id,
                accounts.name,
                COALESCE(SUM(transactions.amount), 0) AS balance,
                accounts.user_id
            FROM accounts
            LEFT JOIN transactions ON accounts.id = transactions.account_id
            WHERE accounts.user_id = ?
            GROUP BY accounts.id, accounts.name, accounts.user_id
            """,
            (user_id,)
        )

        accounts = []
        for row in rows:
            accounts.append(
                Account(row["id"], row["name"], row["balance"], row["user_id"]))

        return accounts

    def find_account_by_id(self, account_id):
        """
        Hakee tietokannasta tilin id:n perusteella.

        Args:
            account_id: Haettavan tilin id.

        Returns:
            Account: Account-olio, joka täsmää id:n kanssa, None jos tiliä ei löydy.
        """
        row = db.query_one(
            "SELECT * FROM accounts WHERE id = ?",
            (account_id,)
        )

        if row:
            return Account(row["id"], row["name"], row["balance"], row["user_id"])

        return None

    def delete_account(self, account_id):
        """
        Poistaa tilin id:n perusteella.

        Args:
            account_id: Poistettavan tilin id.

        Returns:
            None
        """
        sql = "DELETE FROM accounts WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (account_id,))
        self._connection.commit()

    def update_account_name(self, account_id, new_name):
        """
        Päivittää tilin nimen tietokannassa.

        Args:
            account_id: Päivitettävän tilin id.
            new_name: Uusi nimi.

        Returns:
            None
        """
        sql = "UPDATE accounts SET name = ? WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (new_name, account_id))
        self._connection.commit()

    def update_account_balance(self, account_id, new_balance):
        """
        Päivittää tilin balanssin.

        Args:
            account_id: Päivitettävän tilin id.
            new_balance: Tilin uusi balanssi.

        Returns:
            None
        """

        sql = "UPDATE accounts SET balance = ? WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (new_balance, account_id))
        self._connection.commit()
