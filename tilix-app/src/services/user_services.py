from src.entities.user import User
from src.repositories.user_repository import UserRepository
from werkzeug.security import check_password_hash


class UserService:
    """
    Luokka, joka mahdollistaa käyttäjien luomisen, hakemisen ja autentikoinnin UserRepositoryn avulla.

    Attributes:
        user_repository: UserRepository-olio, joka toteuttaa käyttäjätietojen hakemisen ja
        päivittämisen tietokannasta.
    """

    def __init__(self, user_repository):
        """Luokan konstruktori, joka käyttää UserRepository-oliota."""
        self._user_repository = user_repository

    def create_user(self, username, password):
        """
        Luo uuden käytttäjän.

        Args:
            username: Uuden käyttäjän käyttäjätunnus.
            password: Uuden käyttäjän salasana.

        Returns:
            User: Uuden käyttäjän tiedot sisältävä User-olio.
        """
        user = User(username, password)
        return self._user_repository.create_user(user)

    def find_user_by_username(self, username):
        """
        Hakee käyttäjän käyttäjätunnuksen perusteella.

        Args:
            username: haettavan käyttäjän käyttäjätunnus.

        Returns:
            User: User-olio, joka täsmää käyttäjätunnuksen kanssa.
        """
        return self._user_repository.find_user_by_username(username)

    def authenticate(self, username, password):
        """
        Autentikoi käyttäjän käyttäjätunnuksen ja salasanan perusteella.

        Args:
            username: autentikoitavan käyttäjän käyttäjätunnus.
            password: autentikoitavan käyttäjän salasana.

        Returns:
            boolean: Jos käyttäjätunnus ja salasana ovat oikein True, muuten False.
        """
        user = self.find_user_by_username(username)

        if not user:
            return False

        return check_password_hash(user.password, password)
