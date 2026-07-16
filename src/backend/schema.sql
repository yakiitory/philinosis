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

    FOREIGN KEY (guild_id)
        REFERENCES guilds(discord_id)
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES users(discord_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS swearjar (
    user_id TEXT PRIMARY KEY,
    count INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (user_id)
        REFERENCES users(discord_id)
        ON DELETE CASCADE
);
