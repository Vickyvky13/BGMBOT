import random 
from pyrogram import filters 
from pyrogram.types import Message 
from unidecode import unidecode 

from InflexMusic import app 
from InflexMusic.misc import SUDOERS 
from InflexMusic.utils.database import ( 
    get_active_chats, 
    get_active_video_chats,
    get_served_chats,
    get_served_users
) 

@app.on_message(filters.command(["vc", "a"]) & SUDOERS) 
async def active_vc_command_handler(client, message): 
    active_chats_message = await generate_active_chats_message() 
    await message.reply(active_chats_message) 

async def generate_active_chats_message(): 
    active_chats_count = str(len(await get_active_chats())) 
    active_video_chats_count = str(len(await get_active_video_chats())) 
    served_chats_count = str(len(await get_served_chats()))
    served_users_count = str(len(await get_served_users()))

    total_chats_count = str(int(active_chats_count) + int(active_video_chats_count)) 

    message = ( 
        "𝗕𝗼𝘁 𝗔𝗰𝘁𝗶𝘃𝗲 𝗖𝗵𝗮𝘁𝘀 𝗜𝗻𝗳𝗼 • 🔊\n" 
        "•━━━━━━━━━━━━━━━━━━•\n" 
        f"🎧 ᴀᴜᴅɪᴏ 🎧 » {active_chats_count} Active\n" 
        "•───────•\n" 
        f"🎥 ᴠɪᴅᴇᴏ 🎥 » {active_video_chats_count} Active\n" 
        "•──────•\n" 
        f"💬 ᴛᴏᴛᴀʟ 💬 » {total_chats_count} Chats\n" 
        "•──────•\n"
        f"📊 𝙎𝙚𝙧𝙫𝙚𝙙 𝘾𝙝𝙖𝙩𝙨 📊\n» Chats » {served_chats_count}\n"
        "•──────•\n"
        f"👥 𝙎𝙚𝙧𝙫𝙚𝙙 𝙐𝙨𝙚𝙧𝙨 👥\n» Users » {served_users_count}\n"
        "•──────•\n"
    ) 
    return message