import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

# Assuming `app` is your initialized client from InflexMusic
from InflexMusic import app 

# Command to tag all members in batches of 5
@app.on_message(filters.command("tagall") & filters.group)
async def tag_all_members(client: Client, message: Message):
    chat_id = message.chat.id
    from_user = message.from_user
    
    # Check if the user has the appropriate permissions (administrator or owner)
    member = await client.get_chat_member(chat_id, from_user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await message.reply("You must be an admin to use this command.")
        return
    
    # Fetch all members from the chat
    members = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot:
            continue
        members.append(member.user.mention)
    
    # Split the members into batches of 5
    batch_size = 5
    for i in range(0, len(members), batch_size):
        tagged_members = " ".join(members[i:i + batch_size])
        await message.reply(tagged_members)
        await asyncio.sleep(2)  # Add a small delay between messages to avoid hitting rate limits

