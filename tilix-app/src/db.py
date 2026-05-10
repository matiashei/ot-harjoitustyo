import sqlite3
import os
from src.config import DATABASE_FILE_PATH


def get_database_connection():
    os.makedirs(os.path.dirname(DATABASE_FILE_PATH), exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_database_connection()

    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance FLOAT NOT NULL,
            user_id INTEGER REFERENCES users(id),
            is_external INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("PRAGMA table_info(accounts)")
    account_columns = [row[1] for row in cursor.fetchall()]
    if "is_external" not in account_columns:
        cursor.execute(
            "ALTER TABLE accounts ADD COLUMN is_external INTEGER NOT NULL DEFAULT 0"
        )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount FLOAT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            from_account_id INTEGER NOT NULL REFERENCES accounts(id),
            to_account_id INTEGER NOT NULL REFERENCES accounts(id)
        )
    """)

    connection.commit()


def execute(sql, params=()):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(sql, params)
    connection.commit()
    connection.close()


def query(sql, params=()):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()


def query_one(sql, params=()):
    rows = query(sql, params)
    return rows[0] if rows else None


def drop_tables():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS accounts")
    cursor.execute("DROP TABLE IF EXISTS users")
    connection.commit()
    connection.close()
