import psutil
import time
import logging
from InflexMusic import app as Client
from pyrogram import filters
from pyrogram.types import Message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Record the start time of the bot
start_time = time.time()

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
    try:
        uptime = time_formatter((time.time() - start_time) * 1000)
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        ram = memory.percent

        TEXT = (
            f"ᴜᴘᴛɪᴍᴇ : {uptime} | ᴄᴘᴜ : {cpu}%\n"
            f"ㅤ╰⊚ ʀᴀᴍ : {ram}%"
        )
        await message.reply(TEXT)

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")