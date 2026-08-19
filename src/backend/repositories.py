from .models import User, Guild
from .database import Database

class BaseRepository:
    def __init__(self, database: Database):
        self.database = database

    def _create_record(
        self,
        data,
        fields: list[str],
        table_name: str,
        db: Database,
    ) -> tuple[bool, str]:
        """Generic create method for any table."""
        caller_name = self.__class__.__name__

        columns = ", ".join(fields)
        placeholders = ", ".join(["?"] * len(fields))

        query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
        """

        params = tuple(getattr(data, field) for field in fields)

        try:
            last_id = db.execute_query(query, params)
            return True, f"{caller_name} record created!"
        except Exception as e:
            return False, f"Failed to create {caller_name.lower()} record."

    def _update_by_id(
        self,
        identifier,
        data,
        table_name: str,
        db: Database,
        allowed_fields: list[str],
        id_field: str = "id",
    ) -> bool:
        """Generic update method for any table by its ID."""
        caller_name = self.__class__.__name__

        fields_to_update = {
            k: v for k, v in data.items()
            if k in allowed_fields
        }

        if not fields_to_update:
            return False

        set_clause = ", ".join(f"{field} = ?" for field in fields_to_update)

        query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE {id_field} = ?
        """

        params = tuple(fields_to_update.values()) + (identifier,)

        try:
            db.execute_query(query, params)
            return True
        except Exception as e:
            return False

class UserRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database)
        self.table_name = "users"
        self.swearjar_table = "swearjar"

    def does_user_exist(self, user_id: str) -> bool:
        query = f"SELECT 1 FROM {self.table_name} WHERE discord_id = ?"
        result = self.database.fetch_one(query, (user_id,))
        return result is not None

    def create(self, user: User) -> tuple[bool, str]:
        """
            Creates a new user record in the database.
            Called after does_user_exist() returns False.

        Args:
            user (User): User dataclass containing fields from message author.

        Returns:
            tuple[bool, str]: A tuple indicating success/failure and a message.
        """
        fields = [
            "discord_id",
            "username",
            "profile_url",
        ]
        success = self._create_record(user, fields, self.table_name, self.database)
        return success

    def ensure_user_record(self, user_id: str, username: str | None = None, profile_url: str | None = None) -> None:
        existing_user = self.database.fetch_one(
            f"SELECT 1 FROM {self.table_name} WHERE discord_id = ?",
            (user_id,),
        )
        if existing_user is None:
            self.database.execute_query(
                f"INSERT INTO {self.table_name} (discord_id, username, profile_url) VALUES (?, ?, ?)",
                (user_id, username or f"unknown-{user_id}", profile_url or ""),
            )

    def get_swear_count(self, user_id: str) -> int:
        """
            Returns swear count of a user from the database
        """
        query = f"SELECT count FROM {self.swearjar_table} WHERE user_id = ?"
        result = self.database.fetch_one(query, (user_id,))
        if result:
            return result['count']
        else:
            return 0

    def increment_swear(self, user_id: str, n: int) -> bool:
        """
            Increments the swear count of a user.

            Args
                user_id (str): Targeted Discord snowflake id.
                n (int): Amount of bad words said.

            Returns:
                bool: Success or failure.
        """
        print(f"[swearjar] increment requested for {user_id} by {n}")
        self.ensure_user_record(user_id)

        # Ensure there is a swearjar entry for this user.
        check_query = f"SELECT 1 FROM {self.swearjar_table} WHERE user_id = ?"
        check_result = self.database.fetch_one(check_query, (user_id,))
        if check_result is None:
            insert_query = f"INSERT INTO {self.swearjar_table} (user_id) VALUES (?)"
            self.database.execute_query(insert_query, (user_id,))

        increment_query = f"UPDATE {self.swearjar_table} SET count = count + ? WHERE user_id = ?"
        rows_affected = self.database.execute_query(increment_query, (n, user_id))
        current_count = self.get_swear_count(user_id)
        print(f"[swearjar] updated {user_id}; rows_affected={rows_affected}; total_count={current_count}")
        return rows_affected > 0
