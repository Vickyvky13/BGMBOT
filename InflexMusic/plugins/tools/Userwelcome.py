from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from InflexMusic import app  # Assuming app is already configured

# If 'app' does not provide the required functionality, use the Pyrogram Client
pyrogram_client = Client("my_bot")

@app.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    group_name = message.chat.title

    for new_member in message.new_chat_members:
        user_id = new_member.id
        username = new_member.username or "No Username"
        full_name = new_member.first_name or "User"

        # Fetch the user's profile photo using the Pyrogram client
        async with pyrogram_client:
            photos = await pyrogram_client.get_profile_photos(new_member.id)
        profile_pic = photos[0].file_id if photos else None

        welcome_text = (
            f"Welcome to our <b>{group_name}</b> 🎉\n\n"
            f"<b>User name</b>: {full_name}\n"
            f"<b>Username</b>: @{username}\n"
            f"<b>User ID</b>: <code>{user_id}</code>\n"
            f"<b>Mention</b>: <a href='tg://user?id={user_id}'>{full_name}</a>"
        )

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join Us", url=f"https://t.me/{message.chat.username}")]]
        )

        if profile_pic:
            await message.reply_photo(
                photo=profile_pic,
                caption=welcome_text,
                parse_mode="HTML",
                reply_markup=button
            )
        else:
            await message.reply_text(
                text=welcome_text,
                parse_mode="HTML",
                reply_markup=button
            )