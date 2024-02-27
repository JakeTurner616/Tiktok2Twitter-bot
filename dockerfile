# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables for Twitter OAuth credentials
ENV API_KEY="xxxxxx"
ENV API_SECRET="xxxxxx"
ENV ACCESS_TOKEN="xxxxxx"
ENV ACCESS_TOKEN_SECRET="xxxxxx"

# Set environment variable for Discord bot token
ENV BOT_TOKEN="xxxxxx"

# Set environment variable for guild IDs
ENV GUILD_IDS="xxxxxx" 

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Uninstall and reinstall Discord libraries to assert wrapper: https://stackoverflow.com/questions/73464299/importerror-cannot-import-name-option-from-discord
RUN pip uninstall discord -y && \
    pip uninstall py-cord -y && \
    pip install discord && \
    pip install py-cord

# Install Selenium and chromedriver
RUN apt-get update && \
    apt-get install -y chromium-driver

# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot when the container launches
CMD ["python", "bot.py"]
