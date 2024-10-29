import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from InflexMusic import app
from InflexMusic.utils.database import get_served_chats

quotes = [
    "ᴍᴜsɪᴄ ɪs ᴛʜᴇ sᴏᴜɴᴅᴛʀᴀᴄᴋ ᴏғ ʏᴏᴜʀ ʟɪғᴇ. 🎧",
    "ᴡʜᴇʀᴇ ᴡᴏʀᴅs ғᴀɪʟ, ᴍᴜsɪᴄ sᴘᴇᴀᴋs. 🎶",
    "ᴍᴜsɪᴄ ɪs ᴛʜᴇ ᴘᴏᴇᴛʀʏ ᴏғ ᴛʜᴇ ᴀɪʀ. 🎤",
    "ʟᴇᴛ ᴛʜᴇ ᴍᴜsɪᴄ ʙᴇ ʏᴏᴜʀ ɢᴜɪᴅᴇ. 🌌",
    "ʟᴏᴠᴇ ɪs ᴛʜᴇ ᴍᴜsɪᴄ ᴏғ ᴛʜᴇ ʜᴇᴀʀᴛ. 💖",
    "ᴇᴠᴇʀʏ ʟᴏᴠᴇ sᴏɴɢ ɪs ᴀ sᴛᴏʀʏ ᴡᴀɪᴛɪɴɢ ᴛᴏ ʙᴇ ᴛᴏʟᴅ. 📖",
    "ᴍᴜsɪᴄ ʙʀɪɴɢs ᴜs ᴛᴏɢᴇᴛʜᴇʀ ɪɴ ᴀ ᴡᴀʏ ᴛʜᴀᴛ ɴᴏᴛʜɪɴɢ ᴇʟsᴇ ᴄᴀɴ. 🤝",
    "ʟᴏᴠᴇ ᴋɴᴏᴡs ɴᴏ ʙᴏᴜɴᴅs ᴡʜᴇɴ ɪᴛ ᴄᴏᴍᴇs ᴛᴏ ᴍᴜsɪᴄ. ❤️",
    "ᴛʜᴇ ʙᴇsᴛ ᴘᴀʀᴛ ᴏғ ᴍᴜsɪᴄ ɪs ᴛʜᴀᴛ ɪᴛ ᴋɴᴏᴡs ɴᴏ ʟᴀɴɢᴜᴀɢᴇ. 🌍",
    "ᴅᴀɴᴄᴇ ᴛᴏ ᴛʜᴇ ʀʜʏᴛʜᴍ ᴏғ ʏᴏᴜʀ ʜᴇᴀʀᴛ. 💃",
    "ʟᴇᴛ ᴛʜᴇ ᴍᴜsɪᴄ ғɪʟʟ ʏᴏᴜʀ sᴏᴜʟ ᴡɪᴛʜ ʟᴏᴠᴇ. 🕊️",
    "ᴍᴜsɪᴄ ɪs ᴛʜᴇ ʙʀɪᴅɢᴇ ʙᴇᴛᴡᴇᴇɴ ᴛʜᴇ ʜᴇᴀʀᴛ ᴀɴᴅ ᴛʜᴇ ᴍɪɴᴅ. 🧠",
    "ᴇᴠᴇʀʏ ɴᴏᴛᴇ ᴄᴀʀʀɪᴇs ᴀ ᴘɪᴇᴄᴇ ᴏғ ᴍʏ ʜᴇᴀʀᴛ. 💞",
    "ᴡʜᴇɴ ɪɴ ᴅᴏᴜʙᴛ, ᴛᴜʀɴ ᴜᴘ ᴛʜᴇ ᴍᴜsɪᴄ. 🔊",
    "ʟᴏᴠᴇ ɪs ʟɪᴋᴇ ᴀ sᴏɴɢ; ɪᴛ ɴᴇᴠᴇʀ ғᴀᴅᴇs ᴀᴡᴀʏ. 🎵",
    "ʟᴇᴛ ʏᴏᴜʀ ʜᴇᴀʀᴛ sɪɴɢ, ᴀɴᴅ ᴛʜᴇ ᴡᴏʀʟᴅ ᴡɪʟʟ ʟɪsᴛᴇɴ. 🌠",
    "ᴍᴜsɪᴄ ɪs ᴛʜᴇ ʜᴇᴀʀᴛʙᴇᴀᴛ ᴏғ ʟᴏᴠᴇ. 💓",
    "ᴇᴠᴇʀʏ ᴍᴇʟᴏᴅʏ ᴛᴇʟʟs ᴀ ʟᴏᴠᴇ sᴛᴏʀʏ. ✨",
    "ᴍᴜsɪᴄ ɪs ᴛʜᴇ ᴜɴɪᴠᴇʀsᴀʟ ʟᴀɴɢᴜᴀɢᴇ ᴏғ ʟᴏᴠᴇ. ❤️",
    "ʟᴇᴛ ᴛʜᴇ ʀʜʏᴛʜᴍ ᴏғ ʟᴏᴠᴇ ᴍᴏᴠᴇ ʏᴏᴜ. 💃",
    "sɪɴɢ ʏᴏᴜʀ ʜᴇᴀʀᴛ ᴏᴜᴛ; ᴛʜᴇ ᴡᴏʀʟᴅ ɴᴇᴇᴅs ᴛᴏ ʜᴇᴀʀ ʏᴏᴜʀ ʟᴏᴠᴇ. 🎶",
    "ᴍᴜsɪᴄ ᴄᴀɴ ʜᴇᴀʟ ᴛʜᴇ ᴡᴏᴜɴᴅs ᴛʜᴀᴛ ʟᴏᴠᴇ ʟᴇᴀᴠᴇs ʙᴇʜɪɴᴅ. 💔",
    "ʟᴇᴛ ʟᴏᴠᴇ ʙᴇ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ. 🎼",
    "ᴇᴠᴇʀʏ ʟᴏᴠᴇ sᴏɴɢ ʜᴏʟᴅs ᴀ ᴍᴇᴍᴏʀʏ. 📅",
    "ᴡʜᴇɴ ʏᴏᴜ ʟᴏᴠᴇ sᴏᴍᴇᴏɴᴇ, ᴛʜᴇɪʀ sᴏɴɢ ɪs ᴀʟᴡᴀʏs ᴘʟᴀʏɪɴɢ ɪɴ ʏᴏᴜʀ ʜᴇᴀʀᴛ. 🎼",
    "ᴍᴜsɪᴄ ɪs ᴛʜᴇ ʟɪɢʜᴛ ᴛʜᴀᴛ ɢᴜɪᴅᴇs ᴜs ᴛʜʀᴏᴜɢʜ ʟᴏᴠᴇ's ᴊᴏᴜʀɴᴇʏ. 🌠",
    "ʟᴏᴠᴇ ɪs ᴀ ᴍᴇʟᴏᴅʏ ᴛʜᴀᴛ ʟɪɴɢᴇʀs ɪɴ ᴛʜᴇ ʜᴇᴀʀᴛ. 🎻",
    "ᴅᴀɴᴄᴇ ʟɪᴋᴇ ɴᴏʙᴏᴅʏ's ᴡᴀᴛᴄʜɪɴɢ, ʟᴏᴠᴇ ʟɪᴋᴇ ʏᴏᴜ'ᴠᴇ ɴᴇᴠᴇʀ ʙᴇᴇɴ ʜᴜʀᴛ. 💃",
    "ᴛʜᴇ ᴍᴀɢɪᴄ ᴏғ ᴍᴜsɪᴄ ɪs ᴛʜᴀᴛ ɪᴛ ᴍᴀᴋᴇs ʏᴏᴜ ғᴇᴇʟ ᴀʟɪᴠᴇ. 🌈",
    "ᴇᴀᴄʜ sᴏɴɢ ɪs ᴀ ᴄʜᴀᴘᴛᴇʀ ɪɴ ᴛʜᴇ sᴛᴏʀʏ ᴏғ ʟᴏᴠᴇ. 📖",
    "ᴍᴜsɪᴄ ᴄᴀɴ ᴇxᴘʀᴇss ᴡʜᴀᴛ ᴡᴏʀᴅs ᴄᴀɴɴᴏᴛ sᴀʏ. 💬",
    "ʟᴇᴛ ʏᴏᴜʀ ʜᴇᴀʀᴛ sɪɴɢ ᴛʜᴇ ʟᴏᴠᴇ ʏᴏᴜ ғᴇᴇʟ. 🎶",
    "ᴇᴠᴇʀʏ ᴄʜᴏʀᴅ sᴛʀᴜᴍᴍᴇᴅ ɪs ᴀ ʜᴇᴀʀᴛʙᴇᴀᴛ ғᴇʟᴛ. 💓",
    "ғɪɴᴅ ᴛʜᴇ ʟᴏᴠᴇ ɪɴ ᴇᴠᴇʀʏ ɴᴏᴛᴇ. 🎶",
    "ʟᴇᴛ ᴛʜᴇ ᴍᴜsɪᴄ ᴏғ ʏᴏᴜʀ sᴏᴜʟ sʜɪɴᴇ ᴛʜʀᴏᴜɢʜ. 🌟",
    "ʟᴏᴠᴇ ɪs ᴛʜᴇ ɢʀᴇᴀᴛᴇsᴛ ʀʜʏᴛʜᴍ ᴏғ ᴀʟʟ. 💞",
    "ʏᴏᴜʀ ʜᴇᴀʀᴛ ɪs ᴀ ᴄᴀɴᴠᴀs; ʟᴇᴛ ᴍᴜsɪᴄ ᴘᴀɪɴᴛ ɪᴛ ᴡɪᴛʜ ʟᴏᴠᴇ. 🎨",
    "ʟɪsᴛᴇɴ ᴛᴏ ᴛʜᴇ ᴍᴜsɪᴄ ᴏғ ʏᴏᴜʀ ʜᴇᴀʀᴛ. 🎧",
    "ʟᴏᴠᴇ ɪs ᴛʜᴇ ʜᴀʀᴍᴏɴʏ ᴛʜᴀᴛ ᴍᴀᴋᴇs ʟɪғᴇ ʙᴇᴀᴜᴛɪғᴜʟ. 🎶",
    "sɪɴɢ ᴛʜᴇ sᴏɴɢ ᴏғ ʏᴏᴜʀ ʜᴇᴀʀᴛ ᴡɪᴛʜ ᴊᴏʏ. 😊",
    "ᴇᴠᴇʀʏ sᴏɴɢ ɪs ᴀ ʟᴏᴠᴇ ʟᴇᴛᴛᴇʀ ᴡᴀɪᴛɪɴɢ ᴛᴏ ʙᴇ ᴏᴘᴇɴᴇᴅ. 💌",
    "ʟᴇᴛ ᴛʜᴇ ᴍᴜsɪᴄ ᴄᴀʀʀʏ ʏᴏᴜ ᴛᴏ ᴘʟᴀᴄᴇs ᴏғ ʟᴏᴠᴇ. 💗",
    "ʟᴏᴠᴇ ɪs ᴛʜᴇ sᴡᴇᴇᴛᴇsᴛ ᴍᴇʟᴏᴅʏ. 🎶",
    "sᴜʀʀᴏᴜɴᴅ ʏᴏᴜʀsᴇʟғ ᴡɪᴛʜ ᴛʜᴇ ᴍᴜsɪᴄ ᴏғ ʟᴏᴠᴇ. ❤️",
    "ʟᴇᴛ ᴇᴠᴇʀʏ ɴᴏᴛᴇ ʙᴇ ᴀ ʀᴇᴍɪɴᴅᴇʀ ᴏғ ʟᴏᴠᴇ's ʙᴇᴀᴜᴛʏ. ✨",
    "ʟᴏᴠᴇ ɪs ʟɪᴋᴇ ᴀ sᴏɴɢ ᴛʜᴀᴛ ɴᴇᴠᴇʀ ᴇɴᴅs. 💞",
    "ᴛʜᴇ ʀʜʏᴛʜᴍ ᴏғ ʟᴏᴠᴇ ɪs ғᴇʟᴛ ɪɴ ᴇᴠᴇʀʏ ʜᴇᴀʀᴛʙᴇᴀᴛ. ❤️",
]


IS_BROADCASTING = False

async def auto_broadcast():
    global IS_BROADCASTING
    IS_BROADCASTING = True

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Click Me", url="https://example.com")]]
    )

    while True:
        sent = 0
        schats = await get_served_chats()
        
        for chat in schats:
            # Select a random quote from the quotes list
            message_text = random.choice(quotes)
            
            try:
                await app.send_message(chat["chat_id"], text=message_text, reply_markup=keyboard)
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                continue
        
        try:
            print(f"Broadcast sent to {sent} chats.")
        except:
            pass

        # Wait for 5 minutes before the next broadcast
        await asyncio.sleep(120)  # Change to 300 seconds (5 minutes)

# Start the auto-broadcast function
app.add_handler(asyncio.create_task(auto_broadcast()))