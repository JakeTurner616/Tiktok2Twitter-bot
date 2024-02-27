# Tiktok2Twitter-bot

This bot allows users to download TikTok videos and upload them to Twitter with optional captions. It also provides functionality to reply to tweets with TikTok videos.

## Setup

### Prerequisites

- Python 3.9 or later installed on your system
- Docker installed (optional, for running in Docker)

### Instructions

1. Clone this repository to your local machine.

    ```bash
    git clone https://github.com/JakeTurner616/Tiktok2Twitter-bot/
    ```

2. Navigate to the project directory.

    ```bash
    cd Tiktok2Twitter-bot
    ```

3. **Set Twitter API Values and Discord Bot Token**

    #### Docker (Recommended)

    If you're using Docker, follow these steps:

    - Open the `Dockerfile` in a text editor.
    - Update the environment variables `API_KEY`, `API_SECRET`, `ACCESS_TOKEN`, `ACCESS_TOKEN_SECRET`, `BOT_TOKEN`, and `GUILD_IDS` with your Twitter API keys, Discord bot token, and guild IDs.
    - Build the Docker image.

        ```bash
        docker build -t Tiktok2Twitter-bot .
        ```

    - Run the Docker container.

        ```bash
        docker run Tiktok2Twitter-bot
        ```

    #### Without Docker

    If you're not using Docker, you need to set the environment variables manually:

    - Set the following environment variables:
        - `API_KEY`: Your Twitter API key.
        - `API_SECRET`: Your Twitter API secret key.
        - `ACCESS_TOKEN`: Your Twitter access token.
        - `ACCESS_TOKEN_SECRET`: Your Twitter access token secret.
        - `BOT_TOKEN`: Your Discord bot token.
        - `GUILD_IDS`: Comma-separated list of guild IDs where the bot will be used.

    For example:

    ```bash
    export API_KEY="your_twitter_api_key"
    export API_SECRET="your_twitter_api_secret"
    export ACCESS_TOKEN="your_twitter_access_token"
    export ACCESS_TOKEN_SECRET="your_twitter_access_token_secret"
    export BOT_TOKEN="your_discord_bot_token"
    export GUILD_IDS="1234567890,0987654321"
    ```

    Then, install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

    Finally, run your bot:

    ```bash
    python bot.py
    ```
