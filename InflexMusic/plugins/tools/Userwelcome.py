from pyrogram import filters, Client
from pyrogram.enums import UserStatus, ParseMode, ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from InflexMusic import app
import config

# Dictionary to store welcome message settings for each chat (group)
WELCOME_SETTINGS = {}

# Function to check if the user is an admin
async def is_admin(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]

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

# Command handler to enable/disable welcome messages in a group (admin only)
@app.on_message(filters.command("welcome") & filters.group)
async def toggle_welcome(client, message):
    if not await is_admin(client, message):
        return await message.reply_text("Only group admins can use this command.")

    if len(message.command) != 2:
        return await message.reply_text("Usage: /welcome [on|off]")

    status = message.command[1].lower()
    chat_id = message.chat.id

    if status == "on":
        WELCOME_SETTINGS[chat_id] = True
        await message.reply_text("Welcome messages have been enabled for this group.")
    elif status == "off":
        WELCOME_SETTINGS[chat_id] = False
        await message.reply_text("Welcome messages have been disabled for this group.")
    else:
        await message.reply_text("Invalid option. Use /welcome [on|off]")

# Event handler for new members joining the group
@app.on_chat_member_updated()
async def welcome_new_member(client, chat_member_updated):
    chat_id = chat_member_updated.chat.id

    # Check if welcome messages are enabled for this chat (default to True)
    welcome_status = WELCOME_SETTINGS.get(chat_id, True)
    if not welcome_status:
        return  # If welcome is disabled, skip

    if not chat_member_updated.new_chat_member:
        return  # Skip if new_chat_member is None

    new_member = chat_member_updated.new_chat_member.user
    chat = chat_member_updated.chat

    # Check if new member's status is 'member', indicating they joined the group
    if chat_member_updated.new_chat_member.status == ChatMemberStatus.MEMBER:
        old_status = chat_member_updated.old_chat_member.status if chat_member_updated.old_chat_member else None

        # Ensure the user wasn't already a member, admin, or owner before joining
        if old_status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            welcome_text = f"""
<b>Welcome to {chat.title}!</b>

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
            button_url = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users"

            if photo_id:
                photo = await app.download_media(photo_id)
                await client.send_photo(
                    chat.id,
                    photo=photo,
                    caption=welcome_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="𝖠𝖽𝖽 𝖬𝖾 𝖨𝗇 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉", url=button_url)]
                    ])
                )
            else:
                await client.send_message(
                    chat.id,
                    welcome_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="𝖠𝖽𝖽 𝖬𝖾 𝖨𝗇 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉", url=button_url)]
                    ])
                )

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
    button_url = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users"
    if not photo_id:
        await m.delete()
        return await message.reply_text(
            userinfo,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="𝖠𝖽𝖽 𝖬𝖾 𝖨𝗇 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉", url=button_url)]
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
    button_url = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users"

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
    button_url = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users"

    await message.reply_text(
        response_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="𝖠𝖽𝖽 𝖬𝖾 𝖨𝗇 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉", url=button_url)]
        ])
    )
