import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

# Function to send a random quote when a user joins a video chat
@app.on_message(filters.video_chat_started)
async def welcome_user(client, message):
    # Check if the user is joining the video chat
    if message.video_chat_started:
        # Get the user who joined
        user = message.from_user
        # Generate a random quote
        random_quote = random.choice(QUOTES)

        # Create a welcome message with a random quote
        welcome_message = f"Welcome, {user.first_name}! Here's a quote for you:\n\n{random_quote}"

        # Send the welcome message to the chat
        await message.reply_text(
            welcome_message,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Video Chat", url="https://t.me/YourVideoChatLink")]]
            ),
            parse_mode=ParseMode.MARKDOWN
        )