import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import VideoChatParticipantsInvited
from InflexMusic import app
import config

# Define the filter for video chat members being invited
@app.on_message(filters.video_chat_members_invited)
async def video_chat_members_invited_handler(client, message):
    # Check if the message contains VideoChatParticipantsInvited
    if message.video_chat_participants_invited:
        invited_participants = message.video_chat_participants_invited.users
        # If the bot itself is mentioned in the invited participants
        for user in invited_participants:
            if user.is_self:
                await message.reply_text(
                    random.choice([
                        "Hey, you've invited me to the video chat!",
                        "Looks like I'm joining the party 🎉",
                        "Thanks for inviting me, let's get started!"
                    ]),
                    parse_mode=ParseMode.MARKDOWN
                )
                break  # Stop further execution if the bot was found
