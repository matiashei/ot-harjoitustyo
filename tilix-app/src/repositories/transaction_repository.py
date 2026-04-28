from src import db
from src.entities.transaction import Transaction


class TransactionRepository:
    """
    Luokka, joka toteuttaa tilitapahtumatietojen hakemisen ja päivittämisen tietokannasta.

    Attributes:
        connection: Tietokantayhteys, joka mahdollistaa SQL-kyselyiden suorittamisen.
    """

    def __init__(self, connection):
        """Luokan konstruktori, joka ottaa tietokantayhteyden."""
        self._connection = connection

    def create_transaction(self, amount, date, description, account_id):
        """
        Luo uuden tilitapahtuman tietokantaan.

        Args:
            amount: Tilitapahtuman summa.
            date: Tilitapahtuman päivämäärä.
            description: Tilitapahtuman kuvaus.
            account_id: Tilitapahtuman tilin id.

        Returns:
            Transaction: Tilitapahtuman tiedot sisältävä Transaction-olio.
        """
        sql = "INSERT INTO transactions (amount, date, description, account_id)VALUES (?, ?, ?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, (amount, date, description, account_id))
        self._connection.commit()

        transaction_id = cursor.lastrowid
        return Transaction(transaction_id, amount, date, description, account_id)

    def find_transactions_by_account_id(self, account_id):
        """
        Hakee tietokannasta kaikki tilitapahtumat tilin id:n perusteella.

        Args:
            account_id: Tilin id, jonka tilitapahtumat haetaan.

        Returns:
            Lista Transaction-olioista, jotka täsmäävät tilin id:n kanssa.
        """

        rows = db.query(
            "SELECT * FROM transactions WHERE account_id = ?",
            (account_id,)
        )

        transactions = []
        for row in rows:
            transactions.append(
                Transaction(row["id"], row["amount"], row["date"],
                            row["description"], row["account_id"]))

        return transactions

    def delete_transaction(self, transaction_id):
        """
        Poistaa tilitapahtuman id:n perusteella.

        Args:
            transaction_id: Poistettavan tilitapahtuman id.

        Returns:
            None
        """
        sql = "DELETE FROM transactions WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (transaction_id,))
        self._connection.commit()

    def delete_transactions_by_account_id(self, account_id):
        """
        Poistaa kaikki tilitapahtumat, jotka kuuluvat tietylle tilille.

        Args:
            account_id: Tilin id, jonka tapahtumat poistetaan.

        Returns:
            None
        """
        sql = "DELETE FROM transactions WHERE account_id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (account_id,))
        self._connection.commit()

    def update_transaction(self, transaction_id, amount, date, description):
        """
        Päivittää tietokannassa olevan tilitapahtuman id:n perusteella.

        Args:
            transaction_id: Päivitettävän tilitapahtuman id.
            amount: Uusi summa.
            date: Uusi päivämäärä.
            description: Uusi kuvaus.

        Returns:
            None
        """
        sql = "UPDATE transactions SET amount = ?, date = ?, description = ? WHERE id = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, (amount, date, description, transaction_id))
        self._connection.commit()

    def find_transaction_by_id(self, transaction_id):
        """
        Hakee tietokannasta tilitapahtuman id:n perusteella.

        Args:
            transaction_id: Haettavan tilitapahtuman id.

        Returns:
            Transaction: Transaction-olio, joka täsmää id:n kanssa, None jos tapahtumaa ei löydy.
        """

        row = db.query_one(
            "SELECT * FROM transactions WHERE id = ?",
            (transaction_id,)
        )

        if row:
            return Transaction(row["id"], row["amount"], row["date"],
                               row["description"], row["account_id"])

        return None
