import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from InflexMusic import app
import config

# Define the filter for video chat members being invited
@app.on_message(filters.video_chat_members_invited)
async def video_chat_members_invited_handler(client, message):
    # Check if the message contains users invited to the video chat
    if message.video_chat_members_invited:
        invited_participants = message.video_chat_members_invited.users
        # Iterate through the invited users
        for user in invited_participants:
            if user.is_self:
                # Check the type of the user who invited the bot
                inviter = message.from_user
                user_type = "admin" if inviter.is_admin else "regular user"
                await message.reply_text(
                    random.choice([
                        f"Hey, {inviter.mention}, you've invited me to the video chat as a {user_type}!",
                        f"Looks like I'm joining the party, {inviter.mention} ({user_type}) 🎉",
                        f"Thanks for inviting me, {inviter.mention}. Let's get started! You're a {user_type}."
                    ]),
                    parse_mode=ParseMode.MARKDOWN
                )
                break  # Stop further execution if the bot was found