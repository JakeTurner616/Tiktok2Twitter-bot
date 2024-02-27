# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables for Twitter OAuth credentials
ENV API_KEY="xxxx"
ENV API_SECRET="xxxx"
ENV ACCESS_TOKEN="xxxx"
ENV ACCESS_TOKEN_SECRET="xxxx"

# Set environment variable for Discord bot token
ENV BOT_TOKEN="xxxx"

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Uninstall and reinstall Discord libraries to assert wrapper: https://stackoverflow.com/questions/73464299/importerror-cannot-import-name-option-from-discord
RUN pip uninstall discord -y && \
    pip uninstall py-cord -y && \
    pip install discord && \
    pip install py-cord

# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot when the container launches
CMD ["python", "bot.py"]