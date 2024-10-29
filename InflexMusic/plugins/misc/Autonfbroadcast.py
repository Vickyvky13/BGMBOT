import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from InflexMusic import app
from InflexMusic.utils.database import get_served_chats

IS_BROADCASTING = False

async def auto_broadcast():
    global IS_BROADCASTING
    IS_BROADCASTING = True

    message_text = "hey hello sir😞😲😕🤥😒💔"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Click Me", url="https://example.com")]]
    )

    while True:
        sent = 0
        schats = await get_served_chats()
        for chat in schats:
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
        await asyncio.sleep(300)

# Start the auto-broadcast function
app.add_handler(asyncio.create_task(auto_broadcast()))