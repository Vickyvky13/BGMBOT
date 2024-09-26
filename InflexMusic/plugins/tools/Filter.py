from pyrogram import filters, Client
import random
from InflexMusic import app  # Assuming your bot client is initialized here

# List of random responses
responses = [
    "Hello!",
    "Hey you!",
    "Tata!",
    "Hi there!",
    "Greetings!",
    "What's up?",
    "Good to see you!",
    "Howdy!"
]

# List of greetings to trigger the bot
greetings = ["hi", "hello", "good morning"]

@app.on_message(filters.text & filters.create(lambda _, __, message: any(greeting in message.text.lower() for greeting in greetings)))
async def greet_user(client: Client, message):
    response = random.choice(responses)
    await message.reply_text(response)
