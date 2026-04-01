from werkzeug.security import generate_password_hash

from src import db
from src.entities.user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_user(self, user):
        password_hash = generate_password_hash(user.password)
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, (user.username, password_hash))
        self._connection.commit()
        user.user_id = cursor.lastrowid
        return user

    def find_user_by_username(self, username):
        row = db.query_one(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        if row:
            return User(row["username"], row["password_hash"], row["id"])

        return None
