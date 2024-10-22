import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from InflexMusic import app
import config

# List of random quotes
QUOTES = [
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Success is not the key to happiness. Happiness is the key to success.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "Your time is limited, so don't waste it living someone else's life.",
    "Success usually comes to those who are too busy to be looking for it."
]

# Function to send a random quote when users are invited to a video chat
@app.on_message(filters.group)  # Filter for group messages
async def welcome_user(client, message):
    # Check if the message has the video_chat_participants_invited attribute
    if message.video_chat_participants_invited:
        # Loop through invited users
        for invited_user in message.video_chat_participants_invited.users:
            # Generate a random quote
            random_quote = random.choice(QUOTES)

            # Create a welcome message with a random quote
            welcome_message = f"Welcome, {invited_user.first_name}! Here's a quote for you:\n\n{random_quote}"

            # Send the welcome message to the chat
            await message.reply_text(
                welcome_message,
                parse_mode=ParseMode.MARKDOWN
            )