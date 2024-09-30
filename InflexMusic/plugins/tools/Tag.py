import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

# Assuming `app` is your initialized client from InflexMusic
from InflexMusic import app 

# Command to tag all members in batches of 10
@app.on_message(filters.command("tagall") & filters.group)
async def tag_all_members(client: Client, message: Message):
    chat_id = message.chat.id
    from_user = message.from_user

    # Check if the user has the appropriate permissions (administrator or owner)
    member = await client.get_chat_member(chat_id, from_user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await message.reply("You must be an admin to use this command.")
        return

    # Get the custom message if provided
    custom_message = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else ""

    # Fetch all members from the chat
    members = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot:
            continue
        members.append(member.user.mention)

    # Split the members into batches of 10
    batch_size = 10
    for i in range(0, len(members), batch_size):
        tagged_members = " ".join(members[i:i + batch_size])
        final_message = f"||{custom_message}||\n\n{tagged_members}" if custom_message else tagged_members
        await message.reply(final_message)
        await asyncio.sleep(5)  # Add a small delay between messages to avoid hitting rate limits