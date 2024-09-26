from pyrogram import filters, Client
import random
from InflexMusic import app  # Assuming your bot client is initialized here

# Set 1: Responses and greetings
responses_set_1 = [
    "Hello!",
    "Hey you!",
    "Tata!",
    "Hi there!",
    "Greetings!",
    "What's up?",
    "Good to see you!",
    "Howdy!"
]

greetings_set_1 = ["Good morning", "morning", "gm"]

# Set 2: Responses and greetings
responses_set_2 = [
    "Good evening!",
    "Hello there!",
    "Evening!",
    "What a pleasant evening!"
]

greetings_set_2 = ["good evening", "evening"]

# Set 3: Responses and greetings
responses_set_3 = [
    "How are you?",
    "Hope you're doing well!",
    "Everything good?",
    "How's it going?"
]

greetings_set_3 = ["good night", "😴", "gn"]

# Handler for Set 1
@app.on_message(filters.text & filters.create(lambda _, __, message: any(greeting in message.text.lower() for greeting in greetings_set_1)))
async def greet_user_set_1(client: Client, message):
    response = random.choice(responses_set_1)
    await message.reply_text(response)

# Handler for Set 2
@app.on_message(filters.text & filters.create(lambda _, __, message: any(greeting in message.text.lower() for greeting in greetings_set_2)))
async def greet_user_set_2(client: Client, message):
    response = random.choice(responses_set_2)
    await message.reply_text(response)

# Handler for Set 3
@app.on_message(filters.text & filters.create(lambda _, __, message: any(greeting in message.text.lower() for greeting in greetings_set_3)))
async def greet_user_set_3(client: Client, message):
    response = random.choice(responses_set_3)
    await message.reply_text(response)
