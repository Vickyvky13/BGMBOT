import psutil
import time
from InflexMusic import app as Client
from pyrogram import filters
from pyrogram.types import Message

# Function to get the invite link of a chat
async def get_invite_link(chat_id):
    try:
        # Retrieve the chat information
        chat = await Client.get_chat(chat_id)
        
        # If the chat already has an invite link, return it
        if chat.invite_link:
            return chat.invite_link
        
        # If the chat has a username, create a t.me link from the username
        if chat.username:
            return f"https://t.me/{chat.username}"
        
        # If no invite link exists, generate a new one
        return await Client.export_chat_invite_link(chat_id)
    except Exception as e:
        print(f"Error: {e}")
        return None

# Command handler for /get
@Client.on_message(filters.command("get", prefixes=["/"]) & filters.private)
async def send_chat_link(client, message: Message):
    # Check if a chat ID is provided
    if len(message.command) == 2:
        chat_id = message.command[1]
        try:
            # Get the invite link
            link = await get_invite_link(chat_id)
            
            # Send the invite link if it exists
            if link:
                await message.reply(f"Here is the invite link for chat ID {chat_id}: {link}")
            else:
                await message.reply("Could not generate or find an invite link for this chat.")
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
    else:
        await message.reply("Please provide a chat ID. Usage: /get <chat_id>")