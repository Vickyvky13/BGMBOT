import psutil
import time
from InflexMusic import app as Client
from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_ID

# Function to get the invite link of a chat
async def get_invite_link(chat_id):
    try:
        # Retrieve the chat information
        chat = await Client.get_chat(chat_id)

        # If the bot is not in the chat, this will raise an error
        if not chat:
            raise Exception("The bot is not a member of the chat.")

        # If the chat already has an invite link, return it
        invite_link = chat.invite_link if chat.invite_link else None

        # If no invite link exists, try to create one
        if not invite_link:
            if chat.username:
                invite_link = f"https://t.me/{chat.username}"
            else:
                invite_link = await Client.export_chat_invite_link(chat_id)

        # Get the group name
        chat_name = chat.title if chat.title else "No name"

        # Get the member count
        member_count = chat.members_count if chat.members_count else "Unknown"

        # Collect the admin list from the async generator
        admins = [admin.user.first_name async for admin in Client.get_chat_members(chat_id, filter="administrators")]
        admin_list = ", ".join(admins) if admins else "No admins"

        return invite_link, chat_name, member_count, admin_list
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None

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
            # Ensure the chat_id is numeric (could be a user ID or group ID)
            chat_id = int(chat_id)

            # Get the invite link, chat name, member count, and admin list
            link, chat_name, member_count, admin_list = await get_invite_link(chat_id)

            # Send the details if available
            if link:
                await message.reply(f"<b>Group Name</b>: {chat_name}\n"
                                    f"<b>Members</b>: {member_count}\n"
                                    f"<b>Admins</b>: {admin_list}\n"
                                    f"<b>Invite Link</b>: {link}", parse_mode="html")
            else:
                await message.reply("Could not generate or find an invite link for this chat.")
        except ValueError:
            await message.reply("Invalid chat ID. Please provide a numeric chat ID.")
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
    else:
        await message.reply("Please provide a chat ID. Usage: /get <chat_id>")