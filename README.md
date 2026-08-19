# philinosis

#### VIDEO DEMO: [Link](https://youtu.be/sNyf6fCDuRA)

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
     python project.py
   ```
   
## Project Structure
In the `backend/` directory, all database and core logic-related code are stored and is imported by the main project source files. The directory stores as follows:

* `models.py` defines the data classes for the `User` and `Guild` objects. It establishes a predictable structure for the state and data flowing between the underlying database and the Discord API layer.
* `database.py` defines the core database management engine used in the program. It automatically executes an external `schema.sql` file using `sqlparse` to seamlessly initialize the database structure. It makes use of `sqlite3.Row` to return records as Python dictionaries, enforces foreign key constraints, and guarantees safe resource management through strict `try/finally` blocks to prevent database locks.
* `repositories.py` defines the implementation of the Repository Design Pattern to cleanly separate the bot's business logic from raw database operations. It makes use of a `BaseRepository` that dynamically constructs safe, parameterized queries, and a `UserRepository` that empowers lazy user registration and utilizes atomic SQL updates for accurate swear counters.
* `lists.py` defines the localized storage module for the `FILIPINO_SWEAR_WORDS` dictionary dataset. It is merely used to cleanly isolate the raw lists of target profanities from the complex application logic to allow for effortless vocabulary updates.
* `moderation.py` defines the chat filtering implementation by compiling advanced regular expression patterns derived from the swear word dataset. It makes use of the `count_profanity` function to evaluate incoming message strings to detect exact matches, common variations, and sneaky bypass attempts.

In the `root` directory, the main Discord bot execution code is stored. The directory stores as follows:

* `project.py` defines the main entry point, which initializes the asynchronous Hikari gateway bot and establishes the live websocket connection to Discord. It makes use of `GuildMessageCreateEvent` triggers to orchestrate the entire lifecycle of a message by passing the text to the moderation layer and dispatching the bot's public call-out responses.
* `test_project.py` defines the Pytest test fixtures as well as the unit tests for the repositories and respective operations done on the database.
