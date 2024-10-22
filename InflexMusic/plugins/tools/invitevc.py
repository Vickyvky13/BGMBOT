import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from InflexMusic import app
import config

# Define the filter for video chat members being invited
@app.on_message(filters.video_chat_members_invited)
async def video_chat_members_invited_handler(client, message):
    # The invited members can be accessed from message.video_chat_members_invited
    invited = message.video_chat_members_invited

    if invited:
        # Iterate through invited users to check if the bot was invited
        for user in invited.users:
            if user.is_self:  # Check if the bot is among the invited users
                inviter = message.from_user  # Get the user who sent the invite

                # Check if the inviter is an admin
                user_type = "admin" if inviter.is_admin else "regular user"

                # Reply with a random message and mention the inviter
                await message.reply_text(
                    random.choice([
                        f"Hey, {inviter.mention}, you've invited me to the video chat as a {user_type}!",
                        f"Looks like I'm joining the party, {inviter.mention} ({user_type}) 🎉",
                        f"Thanks for inviting me, {inviter.mention}. Let's get started! You're a {user_type}."
                    ]),
                    parse_mode=ParseMode.MARKDOWN
                )
                break  # Stop further execution if the bot was found