import os
import hikari
from dotenv import load_dotenv

from src.backend.repositories import UserRepository, Database
from src.backend.moderation import count_profanity
from src.backend.models import User

def main():
    load_dotenv()

    # Initialize Bot and Database
    bot = hikari.GatewayBot(
        token=os.environ["DISCORD_TOKEN"],
        intents=(
            hikari.Intents.GUILDS
            | hikari.Intents.GUILD_MESSAGES
            | hikari.Intents.MESSAGE_CONTENT
        ),
    )
    db = Database()
    user_repo = UserRepository(db)

    @bot.listen(hikari.GuildMessageCreateEvent)
    async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
        content = event.content or ""
        if not should_process_message(event.is_bot, content):
            return
        user = event.author
        user_id = str(user.id)

        if not user_repo.does_user_exist(user_id):
            new_user = create_new_user_object(
                user_id=user_id,
                username=user.username,
                profile_url=str(user.default_avatar_url)
            )
            user_repo.create(new_user)

        profanity_count = count_profanity(content)
        if profanity_count:
            user_repo.increment_swear(user_id, profanity_count)
            total_count = user_repo.get_swear_count(user_id)
            response = format_swear_message(user.mention, total_count)
            await event.message.respond(response)

    bot.run()

def should_process_message(is_bot: bool, content: str) -> bool:
    """Returns False if the message is from a bot or contains no text."""
    if is_bot:
        return False
    if not content.strip():
        return False
    return True

def create_new_user_object(user_id: str, username: str, profile_url: str) -> User:
    """Creates and returns a new User dataclass instance."""
    return User(
        discord_id=user_id,
        username=username,
        profile_url=profile_url
    )

def format_swear_message(mention: str, total_count: int) -> str:
    """Formats the bot's response message."""
    return f"{mention} now has {total_count} swears."

if __name__ == "__main__":
    main()
