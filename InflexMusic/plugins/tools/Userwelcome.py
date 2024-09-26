from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from InflexMusic import app
import random

# List of welcome messages
WELCOME_MESSAGES = [
    "ʙᴇᴇᴘ ʙᴏᴏᴘ! ᴛʜᴇ ᴜsᴇʀ ʜᴀs ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ. ᴡᴇʟᴄᴏᴍᴇ, {}!",
    "ʜᴇʟʟᴏ, {}! ᴛʜʀɪʟʟᴇᴅ ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.",
    "ᴀ ᴡᴀʀᴍ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴏᴜʀ ɴᴇᴡᴇsᴛ ᴍᴇᴍʙᴇʀ! ʟᴇᴛ ᴛʜᴇ ғᴜɴ ʙᴇɢɪɴ, {}!",
    "ɢʀᴇᴇᴛɪɴɢs! ɢʟᴀᴅ ʏᴏᴜ’ᴠᴇ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴ, {}!",
    "ᴡᴇʟᴄᴏᴍᴇ! ᴛʜᴇ ɢʀᴏᴜᴘ ᴊᴜsᴛ ɢᴏᴛ ʙᴇᴛᴛᴇʀ ᴡɪᴛʜ ʏᴏᴜ ʜᴇʀᴇ, {}.",
    "ʜᴇʟʟᴏ! ʀᴇᴀᴅʏ ᴛᴏ ᴇɴᴊᴏʏ ᴛʜᴇ ɢʀᴏᴜᴘ, {}?",
    "ᴡᴇʟᴄᴏᴍᴇ, {}! ᴡᴇ'ʀᴇ ᴇxᴄɪᴛᴇᴅ ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ ʜᴇʀᴇ.",
]

# List of goodbye messages
GOODBYE_MESSAGES = [
    "{} ʜᴀs ʟᴇғᴛ ᴛʜᴇ ᴄʜᴀᴛ. ғᴀʀᴇᴡᴇʟʟ!",
    "ᴛʜᴀɴᴋ ʏᴏᴜ, {}. ɢᴏᴏᴅʙʏᴇ!",
    "{} ʜᴀs ʟᴇғᴛ ᴜs. ᴡɪsʜɪɴɢ ʏᴏᴜ ᴀʟʟ ᴛʜᴇ ʙᴇsᴛ!",
]

@app.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    for new_member in message.new_chat_members:
        user_mention = new_member.mention
        random_welcome_message = random.choice(WELCOME_MESSAGES).format(user_mention)
        
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
                        "Vɪsɪᴛ",
                        url="https://t.me/solotreee"
                    )
                ]
            ]
        )

        # Send welcome message with user's profile picture or default photo
        if profile_photo:
            await message.reply_photo(
                photo=profile_photo,
                caption=random_welcome_message,
                reply_markup=keyboard
            )
        else:
            await message.reply_text(
                random_welcome_message,
                reply_markup=keyboard
            )

@app.on_message(filters.left_chat_member)
async def goodbye_member(client, message: Message):
    user_mention = message.left_chat_member.mention
    random_goodbye_message = random.choice(GOODBYE_MESSAGES).format(user_mention)
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Vɪsɪᴛ",
                    url="https://t.me/solotreee"
                )
            ]
        ]
    )

    await message.reply_text(
        random_goodbye_message,
        reply_markup=keyboard
    )