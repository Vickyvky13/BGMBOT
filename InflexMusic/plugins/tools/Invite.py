import random
from pyrogram import filters
from pyrogram.types import Message
from unidecode import unidecode
from InflexMusic import app
from InflexMusic.misc import SUDOERS
from InflexMusic.utils.database import (
    get_active_chats, 
    get_active_video_chats,
    get_served_chats,
    get_served_users
)

# Function to get the invite link of a chat
async def get_invite_link(client, chat_id):
    try:
        # Fetch the chat first to ensure bot is in the chat
        chat = await client.get_chat(chat_id)
        
        # Check if the bot has an existing invite link
        if not chat.invite_link:
            # Bot must be an admin to export invite links
            invite_link = await client.export_chat_invite_link(chat_id)
        else:
            invite_link = chat.invite_link
        return invite_link
    
    except Exception as e:
        return str(e)

@app.on_message(filters.command(["getlink"]) & SUDOERS)
async def get_group_link(client, message: Message):
    try:
        # Extract the chat ID from the message or reply
        if message.reply_to_message:
            chat_id = message.reply_to_message.chat.id
        else:
            chat_id = message.chat.id
        
        # Get the invite link for the chat
        invite_link = await get_invite_link(client, chat_id)

        # Send the invite link as a response to the user
        await message.reply(f"Here is the invite link for the chat: {invite_link}")
    
    except Exception as e:
        await message.reply(f"Error: {str(e)}")