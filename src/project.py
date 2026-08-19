from backend.repositories import UserRepository, Database
from backend.moderation import count_profanity
import os
from dotenv import load_dotenv
import hikari

from backend.models import User

load_dotenv()

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
    # Ignore bots
    if event.is_bot:
        return

    user = event.author
    user_id = str(user.id)
    if not user_repo.does_user_exist(user_id):
        new_user = User(
            discord_id=user_id,
            username=user.username,
            profile_url=str(user.default_avatar_url)
        )
        user_repo.create(new_user)

    content = (event.content or "")
    profanity_count = count_profanity(content)
    if profanity_count:
        user_repo.increment_swear(user_id, profanity_count)
        total_count = user_repo.get_swear_count(user_id)
        await event.message.respond(
            f"{user.mention} now has {total_count} swears."
        )

bot.run()
