# philinosis

#### VIDEO DEMO:

#### Description:
A simple profanity checking Discord bot written in Python, using the Hikari API. It can be added to a server to which it should start counting the profanity said by a user, with an emphasis on counting profanity in the Filipino language. Entries and data is persisted in a local SQLite database.

## Features
- **Profanity Detection**: Detects a comprehensive list of Filipino swear words using regular expressions.
- **Automated Swear Jar**: Automatically increments a user's swear count in the database every time they use a tracked word.
- **Real-time Feedback**: Responds to the user in the server with their newly updated total swear count.
- **Automatic User Registration**: Seamlessly registers new users into the database upon their first message or interaction.

## Tech Stack
- **Language:** Python
- **Discord API Wrapper:** Hikari
- **Database:** SQLite3
- **Environment Management:** python-dotenv
- **SQL Parsing:** sqlparse
- **Testing:** pytest

## Installation:
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yakiitory/philinosis.git](https://github.com/yakiitory/philinosis.git)
   cd philinosis
   ```
   
2. **Set up a virtual environment (Recommended):**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
   ```
3. **Install Dependencies:**
  ```bash
     pip install -r requirements.txt
  ```

4. **Environment Configuration:**
Create a `.env` file in the root directory and add your Discord bot token:
   ```DISCORD_TOKEN=your_discord_bot_token_here```

5. **Run the bot:**
At the root directory, run:
   ```bash
     python src/project.py
   ```
   
## Project Structure
- `backend/models.py`: Contains data classes defining the `User` and `Guild` objects.
- `backend/database.py`: Manages the SQLite database connection, transaction handling, and automated schema initialization (using an external `schema.sql`).
- `backend/repositories.py`: Contains the `BaseRepository` and `UserRepository` that handle data access, user creation, and swear count database updates.
- `backend/lists.py`: Stores the `FILIPINO_SWEAR_WORDS` set containing the dictionary of profanities.
- `backend/moderation.py`: Compiles regex patterns from the swear word list and provides the `count_profanity` function to evaluate incoming messages.
- `project.py`: Initializes the Hikari gateway bot, listens for `GuildMessageCreateEvent`, and orchestrates the user tracking and moderation responses.
- `tests/`: Contains pytest fixtures (like the isolated SQLite database connection) and unit tests for database interactions, user creation logic, and swear count increments.
