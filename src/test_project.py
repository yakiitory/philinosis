import pytest
import sqlite3
from dataclasses import dataclass

from backend.database import Database
from backend.repositories import UserRepository
from backend.models import User


@pytest.fixture
def db(tmp_path):
    """
        Isolated SQLite database connection for testing.
    """
    db_file = tmp_path / "test_database.db"
    db_instance = Database(database_path=str(db_file))

    # Initialize test schema using the exact production tables
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        discord_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        profile_url TEXT
    );

    CREATE TABLE IF NOT EXISTS guilds (
        discord_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        welcome_channel_id TEXT,
        logs_channel_id TEXT
    );

    CREATE TABLE IF NOT EXISTS guild_members (
        guild_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        PRIMARY KEY (guild_id, user_id),
        FOREIGN KEY (guild_id) REFERENCES guilds(discord_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(discord_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS swearjar (
        user_id TEXT PRIMARY KEY,
        count INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(discord_id) ON DELETE CASCADE
    );
    """
    cursor = db_instance.connection.cursor()
    cursor.executescript(schema)
    db_instance.connection.commit()
    cursor.close()

    yield db_instance

    db_instance.close()


@pytest.fixture
def user_repo(db:Database):
    """
    Fixture to provide a UserRepository instance for testing.
    """
    return UserRepository(database=db)

# Test Methods
def test_does_user_exist_returns_false_when_empty(user_repo):
    assert user_repo.does_user_exist("123456789") is False


def test_create_user_success(user_repo):
    new_user = User(
            discord_id="123456789",
            username="TestUser",
            profile_url="https://example.com/avatar.png",
        )
    success, message = user_repo.create(new_user)

    assert success is True
    assert "record created" in message
    assert user_repo.does_user_exist("123456789") is True


def test_create_duplicate_user_fails(user_repo):
    new_user = User(
            discord_id="123456789",
            username="TestUser",
            profile_url="https://example.com/avatar.png",
        )
    user_repo.create(new_user)

    # Attempt inserting the same user again, which should fail due to PRIMARY KEY constraint
    success, message = user_repo.create(new_user)
    assert success is False
    assert "Failed to create" in message


def test_get_swear_count_returns_zero_for_new_user(user_repo):
    assert user_repo.get_swear_count("123456789") == 0


def test_increment_swear_creates_user_and_increments_count(user_repo):
    discord_id = "555666777"

    # User does not exist beforehand
    assert user_repo.does_user_exist(discord_id) is False

    # Increment by 3
    result = user_repo.increment_swear(user_id=discord_id, n=3)

    assert result is True
    assert user_repo.does_user_exist(discord_id) is True
    assert user_repo.get_swear_count(discord_id) == 3


def test_increment_swear_multiple_times(user_repo):
    discord_id = "555666777"

    user_repo.increment_swear(user_id=discord_id, n=2)
    user_repo.increment_swear(user_id=discord_id, n=5)

    assert user_repo.get_swear_count(discord_id) == 7
