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

@app.on_message(filters.text & filters.command(["hi"]))
async def greet_user(client: Client, message):
    response = random.choice(responses)
    await message.reply_text(response)
