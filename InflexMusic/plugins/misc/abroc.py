import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from InflexMusic import app
from InflexMusic.misc import SUDOERS
from InflexMusic.utils.database import get_served_chats, get_served_users
from InflexMusic.utils.decorators.language import language

IS_BROADCASTING = False
BROADCAST_INTERVAL = 5 * 60  # 5 minutes in seconds

# Global variable to hold the auto-broadcast task
auto_broadcast_task = None

async def broadcast_message(client, message, query=None, y=None, x=None):
    global IS_BROADCASTING
    IS_BROADCASTING = True
    sent, pin, susr = 0, 0, 0

    if "-user" in message.text:
        served_users = [int(user["user_id"]) for user in await get_served_users()]
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
        schats = await get_served_chats()
        chats = [int(chat["chat_id"]) for chat in schats]
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

    IS_BROADCASTING = False

@app.on_message(filters.command("nfbroadcast") & SUDOERS)
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
        query = query.replace("-pin", "").replace("-nobot", "").replace("-pinloud", "").replace("-assistant", "").replace("-user", "")
        if query == "":
            return await message.reply_text(_["broad_8"])

    await message.reply_text(_["broad_1"])
    asyncio.create_task(broadcast_message(client, message, query, y, x))

async def schedule_broadcast(client, message, _):
    while True:
        await asyncio.sleep(BROADCAST_INTERVAL)
        await broadcast_message(client, message, query="Your broadcast message here", y=None, x=None)

@app.on_message(filters.command("abroadcast") & SUDOERS)
@language
async def start_auto_broadcast(client, message, _):
    global auto_broadcast_task
    if auto_broadcast_task is not None:
        return await message.reply_text("Auto-broadcast is already running.")
    
    await message.reply_text("Auto-broadcast started!")
    auto_broadcast_task = asyncio.create_task(schedule_broadcast(client, message, _))

@app.on_message(filters.command("stopbroadcast") & SUDOERS)
@language
async def stop_auto_broadcast(client, message, _):
    global auto_broadcast_task
    if auto_broadcast_task is None:
        return await message.reply_text("No auto-broadcast is currently running.")
    
    auto_broadcast_task.cancel()  # Cancel the task
    auto_broadcast_task = None  # Reset the global variable
    await message.reply_text("Auto-broadcast stopped!")