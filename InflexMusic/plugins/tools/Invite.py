from pyrogram import filters
from pyrogram.types import Message
from InflexMusic import app
from InflexMusic.misc import SUDOERS

# Function to get the invite link of a chat
async def get_invite_link(client, chat_id):
    try:
        # Fetch chat details to ensure the bot is in the chat
        chat = await client.get_chat(chat_id)

        # Check if the chat is a group or supergroup
        if chat.type not in ["supergroup", "group"]:
            return "This is not a group or supergroup."

        # Check if bot is admin
        member = await client.get_chat_member(chat_id, "me")
        if not member.can_invite_users:
            return "I need the 'Invite Users via Link' permission to generate an invite link."

        # Try to get an existing invite link
        if not chat.invite_link:
            invite_link = await client.export_chat_invite_link(chat_id)
        else:
            invite_link = chat.invite_link

        return invite_link

    except Exception as e:
        return f"Error: {str(e)}"

@app.on_message(filters.command(["getlink"]) & SUDOERS)
async def get_group_link(client, message: Message):
    try:
        # Extract the chat ID from the message or reply
        if message.reply_to_message:
            chat_id = message.reply_to_message.chat.id
        else:
            chat_id = message.chat.id

        # Log the chat_id to help with debugging
        print(f"Fetching invite link for chat_id: {chat_id}")

        # Get the invite link for the chat
        invite_link = await get_invite_link(client, chat_id)

        # Send the invite link as a response to the user
        await message.reply(f"Here is the invite link for the chat: {invite_link}")

    except Exception as e:
        await message.reply(f"Error: {str(e)}")