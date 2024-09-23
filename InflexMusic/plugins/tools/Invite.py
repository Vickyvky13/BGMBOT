import psutil
import time
from InflexMusic import app as Client
from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_ID

# Function to get the invite link and chat details of a chat
async def get_chat_details(chat_id):
    try:
        # Retrieve the chat information
        chat = await Client.get_chat(chat_id)

        # If the chat has an invite link, use it
        invite_link = chat.invite_link
        
        # If no invite link exists, generate a new one
        if not invite_link:
            if chat.username:
                invite_link = f"https://t.me/{chat.username}"
            else:
                invite_link = await Client.export_chat_invite_link(chat_id)

        # Get chat details
        chat_name = chat.title if chat.title else "No name"
        member_count = chat.members_count if chat.members_count else "Unknown"
        
        return invite_link, chat_name, member_count
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

# Command handler for /get
@Client.on_message(filters.command("get", prefixes=["/"]) & filters.private)
async def send_chat_link(client, message: Message):
    # Ensure the user is the owner
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    # Check if a chat ID is provided
    if len(message.command) == 2:
        chat_id = message.command[1]
        try:
            # Get the invite link, chat name, and member count
            link, chat_name, member_count = await get_chat_details(chat_id)
            
            # Send the invite link if it exists
            if link:
                await message.reply(f"<b>Group Name</b>: {chat_name}\n"
                                    f"<b>Members</b>: {member_count}\n"
                                    f"<b>Invite Link</b>: {link}", parse_mode="html")
            else:
                await message.reply("Could not generate or find an invite link for this chat.")
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
    else:
        await message.reply("Please provide a chat ID. Usage: /get <chat_id>")