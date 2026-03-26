import db
from entities.user import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_user(self, user):
        password_hash = generate_password_hash(user.password)
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, (user.username, password_hash))

    def find_user_by_username(self, username):
        row = db.query_one(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        if row:
            return User(row["username"], row["password_hash"])

        return None