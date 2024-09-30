import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

# Initialize your bot client (ensure you replace the correct app instance)
from InflexMusic import app 

spam_chats = []

# Command to tag all members in the group
@app.on_message(filters.command(["tagall", "all"]) & filters.group)
async def mention_all(client: Client, message: Message):
    chat_id = message.chat.id

    # Check if the user is an admin
    user_status = (await client.get_chat_member(chat_id, message.from_user.id)).status
    if user_status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("**Only admins can mention all!**")

    # Handle cases where both text and reply message are given
    if message.command and message.reply_to_message:
        return await message.reply_text("**Give me only one argument!**")

    # Handle command with argument
    if message.command:
        mode = "text_on_cmd"
        msg = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    # Handle reply case
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if msg is None:
            return await message.reply_text(
                "**I can't mention members for older messages! (messages which were sent before I'm added to the group)**"
            )
    else:
        return await message.reply_text("**Reply to a message or give me some text to mention others!**")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""

    # Iterating through chat members
    async for usr in client.get_chat_members(chat_id):
        if chat_id not in spam_chats:
            break
        usrnum += 1
        usrtxt += f"<a href='tg://user?id={usr.user.id}'>{usr.user.first_name}</a>, "

        # Send message in chunks of 5 users
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{msg}\n{usrtxt}"
                await client.send_message(chat_id, txt, parse_mode="html")  # Changed to "html"
            elif mode == "text_on_reply":
                await msg.reply_text(usrtxt, parse_mode="html")  # Changed to "html"
            await asyncio.sleep(3)  # delay between batches
            usrnum = 0
            usrtxt = ""

    # Remove chat from spam list after completion
    try:
        spam_chats.remove(chat_id)
    except ValueError:
        pass

# Command to cancel tagging
@app.on_message(filters.command("cancel") & filters.group)
async def cancel_spam(client: Client, message: Message):
    chat_id = message.chat.id

    # Check if there is an ongoing process in the chat
    if chat_id not in spam_chats:
        return await message.reply_text("**There is no process ongoing...**")

    # Check if user is an admin
    user_status = (await client.get_chat_member(chat_id, message.from_user.id)).status
    if user_status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("**Only admins can execute this command!**")

    # Cancel the mention process
    try:
        spam_chats.remove(chat_id)
    except ValueError:
        pass
    return await message.reply_text("**Stopped mentioning users.**")