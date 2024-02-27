"""
Discord Bot with TikTok Video Downloader and Twitter Integration

This bot allows users to download TikTok videos and upload them to Twitter with optional captions.
It also provides functionalites to tweet or reply to tweets with TikTok videos through discord.

Author: Jake Turner
Date: February 2024
LICENSE: GNU GPL v3.0
"""
import os
import tweepy
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import discord
import re
from discord import Option  # Import Option for defining command options
from selenium.webdriver.chrome.options import Options

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Environment variables for OAuth 1.0a credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
GUILD_IDS = os.getenv("GUILD_IDS").split(",") if os.getenv("GUILD_IDS") else []

# Function to upload video to Twitter


def upload_video_to_twitter(video_path):
    try:
        auth = tweepy.OAuth1UserHandler(
            API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        media = api.media_upload(video_path, media_category='tweet_video')
        return media.media_id_string
    except tweepy.TweepError as e:
        print("Error uploading video to Twitter:", e)
        return None

# Function to tweet video with option to reply
def tweet_video(media_id, tweet_text="Uploading a video via Tweepy!", reply_to_tweet_id=None):
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    try:
        tweet_fields = {"media_ids": [media_id]}
        if reply_to_tweet_id:
            # Correctly setting up the dictionary for a reply
            # Fixed to directly assign the reply ID
            tweet_fields["in_reply_to_tweet_id"] = reply_to_tweet_id

        response = client.create_tweet(text=tweet_text, **tweet_fields)
        if response.data and 'id' in response.data:
            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/user/status/{tweet_id}"
            return tweet_url
        else:
            print("Tweet posted but no ID returned.")
            return None
    except Exception as e:
        print(f"Failed to post reply tweet: {e}")
        return None


# Function to download TikTok video
def download_tiktok_video(tiktok_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Specifies the headless option
    # Disables GPU hardware acceleration
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    # Overcome limited resource problems
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Load the webpage
        driver.get("https://snaptik.app/")

        # Find the input field and submit button
        input_field = driver.find_element(By.ID, "url")
        submit_button = driver.find_element(By.CLASS_NAME, "button-go")

        # Pass TikTok link to the input field
        input_field.send_keys(tiktok_url)

        # Click on the submit button
        submit_button.click()

        # Wait for the download link to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "download-file"))
        )

        # Extract the direct download link
        soup = BeautifulSoup(driver.page_source, "html.parser")
        download_link_element = soup.find("a", class_="download-file")
        if download_link_element:
            download_link = download_link_element["href"]
            # Download the video
            video_response = requests.get(download_link)
            with open("video.mp4", "wb") as video_file:
                video_file.write(video_response.content)
            print("Video downloaded successfully!")
            return True
        else:
            print("Download link element not found.")
            return False

    except Exception as ex:
        print("An error occurred:", ex)
        return False

    finally:
        # Close the webdriver
        driver.quit()


@bot.slash_command(
    name="tiktok",
    description="Download a TikTok video and tweet it with an optional caption",
    guild_ids=GUILD_IDS
)
async def tiktok(
    interaction: discord.Interaction,
    tiktok_url: str = Option(description="Enter the TikTok video URL"),
    caption: str = Option(
        description="Enter a caption for your tweet", default=None, required=False)
):
    # Acknowledge the command
    await interaction.response.defer(ephemeral=False)

    success = download_tiktok_video(tiktok_url)
    if success:
        video_path = 'video.mp4'
        media_id = upload_video_to_twitter(video_path)
        if media_id:
            # Use provided caption or an empty string
            tweet_text = caption if caption else ""
            tweet_url = tweet_video(media_id, tweet_text)
            if tweet_url:
                await interaction.followup.send(f"Video uploaded and tweeted successfully! View it at: {tweet_url}")
            else:
                await interaction.followup.send("Failed to post tweet. Please check the logs for details.")
        else:
            await interaction.followup.send("Failed to upload video to Twitter. Please check the logs for details.")
    else:
        await interaction.followup.send("Failed to download the TikTok video.")


@bot.slash_command(
    name="tiktokreply",
    description="Download a TikTok video and reply to a tweet with it",
    guild_ids=GUILD_IDS
)
async def tiktokreply(
    interaction: discord.Interaction,
    tiktok_url: str = Option(description="Enter the TikTok video URL"),
    twitter_url: str = Option(description="Enter the Twitter URL to reply to"),
    caption: str = Option(
        description="Enter a caption for your tweet", default="")
):
    # Ensure to respond to acknowledge the command
    # Use defer if the operation might take longer
    await interaction.response.defer(ephemeral=False)

    # Extract Tweet ID from the provided Twitter URL
    tweet_id_match = re.search(r"status/(\d+)", twitter_url)
    if tweet_id_match:
        tweet_id = tweet_id_match.group(1)
    else:
        await interaction.followup.send("Invalid Twitter URL provided.", ephemeral=False)
        return

    success = download_tiktok_video(tiktok_url)
    if success:
        video_path = 'video.mp4'
        media_id = upload_video_to_twitter(video_path)
        if media_id:
            tweet_text = caption  # Use provided caption or an empty string
            tweet_url = tweet_video(
                media_id, reply_to_tweet_id=tweet_id, tweet_text=tweet_text)
            if tweet_url:
                await interaction.followup.send(f"Video replied successfully! View it at: {tweet_url}", ephemeral=False)
            else:
                await interaction.followup.send("Failed to post reply tweet. Please check the logs for details.", ephemeral=False)
        else:
            await interaction.followup.send("Failed to upload video to Twitter. Please check the logs for details.", ephemeral=False)
    else:
        await interaction.followup.send("Failed to download the TikTok video.", ephemeral=False)

# hello world to base slash commands on

@bot.slash_command(name="helloworld", description="Hello world", guild_ids=GUILD_IDS,)
async def usage(interaction: discord.Interaction):
    # Create the "Command usage" embed
    initial_embed = discord.Embed(
        title="Hello world!",
        color=discord.Color.blue()
    )
    # Send the initial "Command usage" embed as a response to the slash command
    await interaction.response.send_message(embed=initial_embed, ephemeral=True)


# Your Discord bot token
YOUR_BOT_TOKEN = os.getenv("BOT_TOKEN")
# Run the bot
bot.run(YOUR_BOT_TOKEN)
