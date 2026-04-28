from werkzeug.security import generate_password_hash

from src import db
from src.entities.user import User


class UserRepository:
    """
    Luokka, joka toteuttaa käyttäjätietojen hakemisen ja päivittämisen tietokannasta.
    """

    def __init__(self, connection):
        """Luokan konstruktori, joka muodostaa tietokantayhteyden."""
        self._connection = connection

    def create_user(self, user):
        """
        Luo uuden käyttäjän tietokantaan.

        Args:
            user: User-olio, joka sisältää uuden käyttäjän tiedot.

        Returns:
            User: Uuden käyttäjän tiedot sisältävä User-olio.
        """
        password_hash = generate_password_hash(user.password)
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, (user.username, password_hash))
        self._connection.commit()
        user.user_id = cursor.lastrowid
        return user

    def find_user_by_username(self, username):
        """
        Hakee käyttäjän käyttäjätunnuksen perusteella.

        Args:
            username: haettavan käyttäjän käyttäjätunnus.

        Returns:
            User: User-olio, joka täsmää käyttäjätunnuksen kanssa, None jos käyttäjää ei löydy.
        """
        row = db.query_one(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        if row:
            return User(row["username"], row["password_hash"], row["id"])

        return None
