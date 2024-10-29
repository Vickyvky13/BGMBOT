import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from InflexMusic import app
from InflexMusic.misc import SUDOERS
from InflexMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from InflexMusic.utils.decorators.language import language
from InflexMusic.utils.formatters import alpha_to_int
from config import adminlist

IS_BROADCASTING = False

async def auto_broadcast():
    while True:
        try:
            # Construct message with a URL button
            text = "hey hello sir😞😲😕🤥😒💔"
            button = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Click Here", url="https://example.com")]
                ]
            )
            
            # Get served chats for broadcast
            schats = await get_served_chats()
            chats = [int(chat["chat_id"]) for chat in schats]

            # Loop through and send the message to each chat
            for chat_id in chats:
                try:
                    await app.send_message(chat_id, text=text, reply_markup=button)
                    await asyncio.sleep(0.2)  # Prevent flooding
                except FloodWait as fw:
                    flood_time = int(fw.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except Exception as e:
                    print(f"Error in chat {chat_id}: {e}")
                    continue

            await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds) before broadcasting again
        except Exception as e:
            print(f"Error in auto_broadcast: {e}")
            await asyncio.sleep(300)  # Prevent crash, wait before retrying

@app.on_message(filters.command("ntg") & SUDOERS)
@language
async def nfbraodcast_message(client, message, _):
    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_2"])
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text(_["broad_8"])

    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for user in susers:
            served_users.append(int(user["user_id"]))
        for i in served_users:
            try:
                m = (
                    await app.copy_message(chat_id=i, from_chat_id=y, message_id=x, reply_markup=message.reply_to_message.reply_markup, protect_content=True)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                pass
        try:
            await message.reply_text(_["broad_4"].format(susr))
        except:
            pass

    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = (
                    await app.copy_message(chat_id=i, from_chat_id=y, message_id=x, reply_markup=message.reply_to_message.reply_markup, protect_content=True)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        continue
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
            await message.reply_text(_["broad_3"].format(sent, pin))
        except:
            pass

# Start the auto_broadcast function as a background task when the app starts
app.add_handler(asyncio.create_task(auto_broadcast()))