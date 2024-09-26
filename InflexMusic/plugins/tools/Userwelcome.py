from pyrogram import filters, Client
from pyrogram.enums import UserStatus, ParseMode, ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from InflexMusic import app
import config

# Function to get the user status
def get_user_status(status):
    if status == UserStatus.ONLINE:
        return "online"
    elif status == UserStatus.OFFLINE:
        return "User is offline"
    elif status == UserStatus.RECENTLY:
        return "last seen recently"
    elif status == UserStatus.LAST_WEEK:
        return "last seen within a week"
    elif status == UserStatus.LAST_MONTH:
        return "last seen within a month"
    else:
        return "last seen a long time ago"

# Command handler to fetch user info
@app.on_message(filters.command(["info", f"info@{app.username}"]))
async def info_user(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) == 1:
        user_id = message.from_user.id
    else:
        user_id = message.text.split(None, 1)[1]

    m = await message.reply_text("Getting user info...")
    user = await app.get_users(user_id)
    status = user.status

    userinfo = f"""
<b><u>User Info</u></b>
<b>User ID:</b> <code>{user.id}</code>
<b>First Name:</b> {user.first_name}
<b>Last Name:</b> {user.last_name if user.last_name else ""}
<b>Username:</b> {"@" + user.username if user.username else ""}
<b>Link:</b> {user.mention}
<b>Status:</b> {get_user_status(status)}
<b>DC ID:</b> <code>{user.dc_id}</code>
<b>Premium:</b> <code>{user.is_premium}</code>
<b>Language Code:</b> <code>{user.language_code}</code>
"""

    photo_id = user.photo.big_file_id if user.photo else None
    button_url = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"
    if not photo_id:
        await m.delete()
        return await message.reply_text(
            userinfo,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Support Group", url=button_url)]
            ])
        )

    photo = await app.download_media(photo_id)
    await m.delete()
    await message.reply_photo(
        photo,
        caption=userinfo,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Support Group", url=button_url)]
        ])
    )

# Command handler to fetch group and user chat ID
@app.on_message(filters.command("id"))
async def get_ids(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    response_text = f"**Chat ID:** `{chat_id}`\n**Your User ID:** `{user_id}`"
    button_url = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"

    await message.reply_text(
        response_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Support Group", url=button_url)]
        ])
    )

# Command handler to fetch only the user chat ID
@app.on_message(filters.command("myid"))
async def get_my_id(client, message):
    user_id = message.from_user.id
    response_text = f"**Your User ID:** `{user_id}`"
    button_url = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"

    await message.reply_text(
        response_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Support Group", url=button_url)]
        ])
    )

# Event handler for new members joining the group
@app.on_chat_member_updated()
async def welcome_new_member(client, chat_member_updated):
    new_member = chat_member_updated.new_chat_member.user
    chat = chat_member_updated.chat

    # Check if new member's status is 'member', indicating they joined the group
    if chat_member_updated.new_chat_member.status == ChatMemberStatus.MEMBER:
        # Handle cases where old_chat_member might be None (first-time join)
        old_status = chat_member_updated.old_chat_member.status if chat_member_updated.old_chat_member else None

        # Ensure the user wasn't already a member, admin, or owner before joining
        if old_status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            welcome_text = f"""
<b>Welcome to our {chat.title}!</b>

<b><u>User Info</u></b>
<b>User ID:</b> <code>{new_member.id}</code>
<b>First Name:</b> ♮ {new_member.first_name}
<b>Last Name:</b> {new_member.last_name if new_member.last_name else ""}
<b>Username:</b> {"@" + new_member.username if new_member.username else ""}
<b>Link:</b> {new_member.mention}
<b>Status:</b> {get_user_status(new_member.status)}
<b>DC ID:</b> <code>{new_member.dc_id}</code>
<b>Premium:</b> <code>{new_member.is_premium}</code>
<b>Language Code:</b> <code>{new_member.language_code}</code>
"""

            # Fetch the user's profile photo if available
            photo_id = new_member.photo.big_file_id if new_member.photo else None
            button_url = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"

            if photo_id:
                # Download the profile photo
                photo = await app.download_media(photo_id)
                # Send the welcome message along with the user's profile photo
                await client.send_photo(
                    chat.id,
                    photo=photo,
                    caption=welcome_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="Support Group", url=button_url)]
                    ])
                )
            else:
                # Send the welcome message without a photo if the user has no profile picture
                await client.send_message(
                    chat.id,
                    welcome_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="Support Group", url=button_url)]
                    ])
                )
