import psutil
import time
import logging
from InflexMusic import app as Client
from pyrogram import filters
from pyrogram.types import Message
from InflexMusic.utils.database import ( 
    get_active_chats, 
    get_active_video_chats, 
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Record the start time of the bot
start_time = time.time()

# Counter for consecutive zero total_chats
zero_count = 0

# Function to format the uptime in a human-readable format
def time_formatter(milliseconds):
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    tmp = (((str(weeks) + "ᴡ:") if weeks else "") +
           ((str(days) + "ᴅ:") if days else "") +
           ((str(hours) + "ʜ:") if hours else "") +
           ((str(minutes) + "ᴍ:") if minutes else "") +
           ((str(seconds) + "s") if seconds else ""))

    if not tmp:
        return "0s"
    if tmp.endswith(":"):
        return tmp[:-1]

    return tmp

# Define a command handler for the /checker command
@Client.on_message(filters.command("checker"))
async def activevc(_, message: Message):
    global zero_count

    try:
        uptime = time_formatter((time.time() - start_time) * 1000)
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        ram = memory.percent

        active_chats = len(await get_active_chats())
        active_video_chats = len(await get_active_video_chats())
        total_chats = (active_chats + active_video_chats) * 3

        logger.info(f"Active Chats: {active_chats}")
        logger.info(f"Active Video Chats: {active_video_chats}")

        # Check if total_chats is zero and increment the counter
        if total_chats == 0:
            zero_count += 1
        else:
            zero_count = 0  # Reset the counter if total_chats is not zero

        # Prepare the reply message
        TEXT = (
            f"ᴜᴘᴛɪᴍᴇ : {uptime} | ᴄᴘᴜ : {cpu}\n"
            f"ㅤ╰⊚ ʀᴀᴍ : {ram}% | ᴀᴄᴛɪᴠᴇ ᴄʜᴀᴛ : {total_chats}"
        )

        # Check if the counter has reached 5 consecutive zeros
        if zero_count >= 2:
            TEXT += "\nWarning: IP block detected. Active chats count is zero for 5 consecutive checks."
            zero_count = 0  # Reset the counter after sending the IP block message
        
        await message.reply(TEXT)

    except Exception as e:
        logger.error(f"Error in /checker command: {str(e)}")
        await message.reply(f"An error occurred: {str(e)}")