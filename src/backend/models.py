from dataclasses import dataclass

@dataclass
class User:
    discord_id: str
    username: str
    profile_url: str

@dataclass
class Guild:
    discord_id: str
    welcome_channel_id: str
    logs_channel_id: str
