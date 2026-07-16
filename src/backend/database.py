import os
import sqlite3
import sqlparse


class Database:
    """
    Singleton database instance.
    Automatically creates the database and initializes schema.sql.

    Parameters:
        database_path (str): Path to the SQLite database file. Defaults to "database.db".
    """

    def __init__(self, database_path="database.db"):
        if not os.path.isabs(database_path):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            database_path = os.path.join(base_dir, database_path)

        self.database_path = database_path
        print(f"[database] using SQLite database at {self.database_path}")

        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON;")

        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        if os.path.exists(schema_path):
            self.initialize_schema(schema_path)

    def initialize_schema(self, sql_file_path: str):
        with open(sql_file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        statements = sqlparse.split(sql_script)

        cursor = self.connection.cursor()

        for statement in statements:
            stmt = statement.strip()
            if stmt and not stmt.startswith("--"):
                cursor.execute(stmt)

        self.connection.commit()
        cursor.close()

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, params or ())
            self.connection.commit()

            if query.lstrip().upper().startswith("INSERT"):
                return cursor.lastrowid

            return cursor.rowcount

        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, params or ())
            row = cursor.fetchone()
            return dict(row) if row else None

        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, params or ())
            return [dict(row) for row in cursor.fetchall()]

        finally:
            cursor.close()

    def begin_transaction(self):
        self.connection.execute("BEGIN")

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()
