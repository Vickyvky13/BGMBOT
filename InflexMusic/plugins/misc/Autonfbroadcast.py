import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from InflexMusic import app
from InflexMusic.utils.database import get_served_chats

quotes = [
    "𝗙𝗔𝗟𝗟 𝗜𝗡 𝗟𝗢𝗩𝗘 𝗪𝗜𝗧𝗛 𝗘𝗩𝗘𝗥𝗬 𝗕𝗘𝗔𝗧! 🎶 𝗗𝗜𝗦𝗖𝗢𝗩𝗘𝗥 𝗠𝗨𝗦𝗜𝗖 𝗪𝗜𝗧𝗛 {app.mention}.",
    "𝗟𝗘𝗧 𝗠𝗨𝗦𝗜𝗖 𝗔𝗡𝗗 𝗟𝗢𝗩𝗘 𝗙𝗜𝗟𝗟 𝗬𝗢𝗨𝗥 𝗛𝗘𝗔𝗥𝗧. ❤️ 𝗣𝗟𝗔𝗬 𝗢𝗡 𝗪𝗜𝗧𝗛 {app.mention}.",
    "𝗪𝗛𝗘𝗥𝗘 𝗠𝗨𝗦𝗜𝗖 𝗠𝗘𝗘𝗧𝗦 𝗟𝗢𝗩𝗘. 💫 𝗧𝗨𝗡𝗘 𝗜𝗡 𝗧𝗢 {app.mention}.",
    "𝗙𝗘𝗘𝗟 𝗧𝗛𝗘 𝗟𝗢𝗩𝗘 𝗜𝗡 𝗘𝗩𝗘𝗥𝗬 𝗡𝗢𝗧𝗘. 🎼 𝗢𝗡𝗟𝗬 𝗪𝗜𝗧𝗛 {app.mention}.",
    "𝗕𝗘𝗖𝗔𝗨𝗦𝗘 𝗟𝗢𝗩𝗘 𝗦𝗢𝗨𝗡𝗗𝗦 𝗕𝗘𝗧𝗧𝗘𝗥 𝗪𝗜𝗧𝗛 𝗠𝗨𝗦𝗜𝗖. 🎧 𝗧𝗥𝗬 {app.mention}.",
    "𝗕𝗥𝗜𝗡𝗚 𝗟𝗢𝗩𝗘 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗣𝗟𝗔𝗬𝗟𝗜𝗦𝗧. 🎶 𝗢𝗡𝗟𝗬 𝗢𝗡 {app.mention}.",
    "𝗧𝗨𝗥𝗡 𝗨𝗣 𝗧𝗛𝗘 𝗟𝗢𝗩𝗘. 💖 𝗟𝗘𝗧 {app.mention} 𝗣𝗟𝗔𝗬.",
    "𝗧𝗛𝗘 𝗣𝗘𝗥𝗙𝗘𝗖𝗧 𝗛𝗔𝗥𝗠𝗢𝗡𝗬 𝗢𝗙 𝗠𝗨𝗦𝗜𝗖 𝗔𝗡𝗗 𝗟𝗢𝗩𝗘, 🎶 𝗥𝗜𝗚𝗛𝗧 𝗛𝗘𝗥𝗘 𝗢𝗡 {app.mention}.",
    "𝗪𝗛𝗘𝗡 𝗠𝗨𝗦𝗜𝗖 𝗜𝗦 𝗬𝗢𝗨𝗥 𝗟𝗢𝗩𝗘 𝗟𝗔𝗡𝗚𝗨𝗔𝗚𝗘, 🥰 𝗧𝗨𝗡𝗘 𝗜𝗡 𝗧𝗢 {app.mention}.",
    "𝗙𝗜𝗡𝗗 𝗬𝗢𝗨𝗥 𝗦𝗢𝗨𝗡𝗗𝗧𝗥𝗔𝗖𝗞 𝗧𝗢 𝗟𝗢𝗩𝗘 🎵 𝗪𝗜𝗧𝗛 {app.mention}.",
    "𝗕𝗘𝗖𝗔𝗨𝗦𝗘 𝗘𝗩𝗘𝗥𝗬 𝗟𝗢𝗩𝗘 𝗦𝗧𝗢𝗥𝗬 𝗗𝗘𝗦𝗘𝗥𝗩𝗘𝗦 𝗔 𝗦𝗢𝗨𝗡𝗗𝗧𝗥𝗔𝗖𝗞. 💖 𝗟𝗜𝗦𝗧𝗘𝗡 𝗪𝗜𝗧𝗛 {app.mention}.",
    "𝗙𝗘𝗘𝗟 𝗧𝗛𝗘 𝗠𝗨𝗦𝗜𝗖. 🎶 𝗙𝗘𝗘𝗟 𝗧𝗛𝗘 𝗟𝗢𝗩𝗘. 𝗝𝗢𝗜𝗡 {app.mention}.",
    "𝗙𝗔𝗟𝗟 𝗜𝗡 𝗟𝗢𝗩𝗘, 𝗢𝗡𝗘 𝗦𝗢𝗡𝗚 𝗔𝗧 𝗔 𝗧𝗜𝗠𝗘. 🎼 𝗢𝗡𝗟𝗬 𝗢𝗡 {app.mention}.",
    "𝗪𝗛𝗘𝗥𝗘 𝗘𝗩𝗘𝗥𝗬 𝗕𝗘𝗔𝗧 𝗜𝗦 𝗔 𝗛𝗘𝗔𝗥𝗧𝗕𝗘𝗔𝗧. ❤️ 𝗗𝗜𝗦𝗖𝗢𝗩𝗘𝗥 {app.mention}.",
    "𝗬𝗢𝗨𝗥 𝗟𝗢𝗩𝗘 𝗙𝗢𝗥 𝗠𝗨𝗦𝗜𝗖 𝗦𝗧𝗔𝗥𝗧𝗦 𝗛𝗘𝗥𝗘. 🎶 𝗟𝗜𝗦𝗧𝗘𝗡 𝗢𝗡 {app.mention}.",
    "𝗕𝗘𝗖𝗔𝗨𝗦𝗘 𝗟𝗢𝗩𝗘 𝗔𝗡𝗗 𝗠𝗨𝗦𝗜𝗖 𝗔𝗥𝗘 𝗜𝗡𝗦𝗘𝗣𝗔𝗥𝗔𝗕𝗟𝗘. 🎧 𝗘𝗫𝗣𝗘𝗥𝗜𝗘𝗡𝗖𝗘 𝗜𝗧 𝗪𝗜𝗧𝗛 {app.mention}.",
    "𝗙𝗜𝗡𝗗 𝗟𝗢𝗩𝗘 𝗜𝗡 𝗘𝗩𝗘𝗥𝗬 𝗦𝗢𝗡𝗚. 🎶 𝗟𝗘𝗧 {app.mention} 𝗟𝗘𝗔𝗗 𝗧𝗛𝗘 𝗪𝗔𝗬.",
    "𝗧𝗨𝗥𝗡 𝗨𝗣 𝗧𝗛𝗘 𝗟𝗢𝗩𝗘 𝗔𝗡𝗗 𝗟𝗘𝗧 𝗧𝗛𝗘 𝗠𝗨𝗦𝗜𝗖 𝗣𝗟𝗔𝗬. 🎶 𝗪𝗜𝗧𝗛 {app.mention}.",
    "𝗧𝗛𝗘 𝗦𝗢𝗨𝗡𝗗𝗧𝗥𝗔𝗖𝗞 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗟𝗢𝗩𝗘 𝗦𝗧𝗢𝗥𝗬 𝗜𝗦 𝗛𝗘𝗥𝗘. 💖 𝗣𝗟𝗔𝗬 𝗢𝗡 {app.mention}.",
    "𝗕𝗘𝗖𝗔𝗨𝗦𝗘 𝗟𝗢𝗩𝗘 𝗜𝗦 𝗠𝗨𝗦𝗜𝗖, 𝗔𝗡𝗗 𝗠𝗨𝗦𝗜𝗖 𝗜𝗦 𝗟𝗢𝗩𝗘. 🎵 𝗣𝗟𝗔𝗬 𝗪𝗜𝗧𝗛 {app.mention}."
]



IS_BROADCASTING = False

async def get_served_chats():
    # Replace this function with actual implementation
    # This should return a list of chats with the format [{"chat_id": chat_id}, ...]
    pass

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
            # Select a random quote and format it with the app's mention
            message_text = random.choice(quotes).replace("{app_mention}", app.mention)

            try:
                await app.send_message(chat["chat_id"], text=message_text, reply_markup=keyboard)
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception as e:
                print(f"Error sending message: {e}")
                continue

        try:
            print(f"Broadcast sent to {sent} chats.")
        except Exception as e:
            print(f"Error printing broadcast summary: {e}")

        # Wait for 5 minutes before the next broadcast
        await asyncio.sleep(300)  # 300 seconds = 5 minutes

# Assume `app` is your pyrogram Client instance
app.add_handler(asyncio.create_task(auto_broadcast()))