from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from InflexMusic import app

@app.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    group_name = message.chat.title  # Get the group name

    for new_member in message.new_chat_members:
        user_mention = new_member.mention
        user_id = new_member.id
        username = f"@{new_member.username}" if new_member.username else "No username"
        
        # Construct the welcome message for the caption
        welcome_message = (
            f"Welcome to {group_name}!\n\n"
            f"**Name**: {user_mention}\n"
            f"**User ID**: `{user_id}`\n"
            f"**Username**: {username}"
        )

        # Fetch the user's profile picture
        try:
            photos = await client.get_profile_photos(new_member.id)
            if photos.total_count > 0:
                profile_photo = photos.photos[0].file_id
            else:
                profile_photo = None  # Fallback if no profile photo is found
        except Exception as e:
            profile_photo = None  # Handle any error

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Visit",
                        url="https://t.me/solotreee"
                    )
                ]
            ]
        )

        # Send welcome message with user's profile picture or text message if no profile photo is available
        if profile_photo:
            await message.reply_photo(
                photo=profile_photo,
                caption=welcome_message,
                reply_markup=keyboard
            )
        else:
            await message.reply_text(
                welcome_message,
                reply_markup=keyboard
            )

@app.on_message(filters.left_chat_member)
async def goodbye_member(client, message: Message):
    # If you still need a goodbye message handler in the future, you can add it here.
    pass