from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from InflexMusic import app

@app.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    # Get the group name from the chat
    group_name = message.chat.title

    # Loop through each new chat member (in case multiple members are added)
    for new_member in message.new_chat_members:
        # Fetch new member details
        user_id = new_member.id
        username = new_member.username or "No Username"
        full_name = new_member.first_name or "User"

        # Welcome message with HTML formatting
        welcome_text = (
            f"Welcome to our <b>{group_name}</b> 🎉\n\n"
            f"<b>User name</b>: {full_name}\n"
            f"<b>Username</b>: @{username}\n"
            f"<b>User ID</b>: <code>{user_id}</code>\n"
            f"<b>Mention</b>: <a href='tg://user?id={user_id}'>{full_name}</a>"
        )

        # Add a button that links to the group's username or any other URL
        button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Join Us", url=f"https://t.me/{message.chat.username}")]
            ]
        )

        # Send plain text welcome message (since profile picture is unavailable)
        await message.reply_text(
            text=welcome_text,
            parse_mode="HTML",  # Set HTML parse mode
            reply_markup=button
        )