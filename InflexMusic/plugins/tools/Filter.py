from pyrogram import filters, Client
import random
from InflexMusic import app  # Assuming your bot client is initialized here

# Set 1: Responses and greetings (Updated with Tamil)
responses_set_1 = [
    "வணக்கம் டா மாப்ள",
    "காலை வணக்கம் தங்கம் 🥰",
    "Good morning my sweetheart",
    "காலங்காத்தால உன்கிட்ட வா நான் குட் மார்னிங் மெசேஜ் வாங்கணும்",
    "காலங்காத்தால இவன் மூஞ்சில முழிக்கிறவன் என்ன நடக்கப் போவதோ தெரியல",
    "உன்கிட்ட யாரு பேசுவா குட் மார்னிங் மெசேஜ் போடுற",
    "குட் மார்னிங் சொன்னது போதும் கிளம்பு",
    "நீ எல்லாம் எதுக்குடா இருக்க எப்ப பார்த்தாலும் குட் மார்னிங் மெசேஜ் போட்டுக்கிட்டே இருக்கியே டா"
]

greetings_set_1 = ["Good morning", "morning", "gm", "காலை வணக்கம்", "invite"]

# Set 2: Responses and greetings (Updated with Tamil)
responses_set_2 = [
    "போறேன் போறேன்னு சொல்ற ஆனா போக மாட்டேங்குறானே இங்கேயே தான் இருக்கான்",
    "சொல்லிட்டு எல்லாம் கிளம்பு காத்து வரட்டும்",
    "இவன் யாரவது கழுத்து புடிச்சு தள்ளி விடுங்களேன், போக மாட்டேங்குறான்",
    "சொல்லிட்ட இல்ல கிளம்பு",
    "மெசேஜ் பண்ணியது போதும் கிளம்பு",
    "இப்ப இருந்து என்ன சாதிச்சிட்டா இப்ப நீங்க மெசேஜ் பண்ணிட்டு இருக்க",
    "யோ குரூப் ஓனர் இவன முதல்ல ban அடங்கிய",
    "நீயா போறியா இல்ல மூஞ்சில ஆசிட் அடிச்சு ஊத்தவா"
]

greetings_set_2 = ["tata", "bye", "na pore", "போ", "டாடா"]

# Set 3: Responses and greetings (Updated with Tamil)
responses_set_3 = [
    "சரி குட் நைட்",
    "சரி சீக்கிரம் தூங்கப்போ. இங்க இருந்து என்ன கழட்ட போற",
    "இவ்வளவு நேரம் இங்கே மெசேஜ் பண்ணி என்ன சாதித்து விட்டான் தெரியல தூங்க போறேன்",
    "என்ன உன்னோட ஆள் கூப்பிடற ஆளா",
    "எப்ப பாத்தாலும் தூங்கிக்கொண்டே போ",
    "சரி சரி கெளம்பு மூஞ்சியும் மொகரையும் போ",
    "தூங்கப் போற மூஞ்ச பாத்தியா"
]

greetings_set_3 = ["good night", "gn", "😴", "குட் நைட்", "தூங்க"]

# Handler for Set 1 (Good Morning Greetings)
@app.on_message(filters.text & filters.create(lambda _, __, message: any(greeting in message.text.lower() for greeting in greetings_set_1)))
async def greet_user_set_1(client: Client, message):
    response = random.choice(responses_set_1)
    await message.reply_text(response)

# Handler for Set 2 (Goodbye Messages)
@app.on_message(filters.text & filters.create(lambda _, __, message: any(greeting in message.text.lower() for greeting in greetings_set_2)))
async def greet_user_set_2(client: Client, message):
    response = random.choice(responses_set_2)
    await message.reply_text(response)

# Handler for Set 3 (Good Night Messages)
@app.on_message(filters.text & filters.create(lambda _, __, message: any(greeting in message.text.lower() for greeting in greetings_set_3)))
async def greet_user_set_3(client: Client, message):
    response = random.choice(responses_set_3)
    await message.reply_text(response)

# List of custom responses when a user leaves the group
leave_responses = [
    "போறான் பாரு! {user} நம்ம குரூப்ப விட்டு கிளம்பிட்டாரு!",
    "படத்தில இருந்து கதாநாயகன் {user} வெளியேறி விட்டார்!",
    "{user}, சரியாப் பாக்காம போறே!",
    "{user} எனக்கா important நீ போயிட்டே!",
    "போய் வா {user}, நெஞ்சம் நிம்மதியா இருக்கட்டும்!",
    "போறேன் என்கிறான் {user}, இனி நம்ம குரூப்புக்கு கிடைக்க மாட்டான்!",
    "{user} அவன் போயிடுவானு நெனச்சியா?"
]

# Custom message when a user leaves the group
@app.on_message(filters.left_chat_member)
async def user_left_group(client: Client, message):
    user_name = message.left_chat_member.first_name  # Get the user's first name
    response = random.choice(leave_responses).format(user=user_name)  # Choose a random response
    await message.reply_text(response)

# List of custom responses when a user is invited to a video chat
video_chat_responses = [
    "வீடியோ காலுக்கு அழைக்கிறாங்க பாரு {user}!",
    "{user}, வீடியோ காலில் கலக்க போறேன்!",
    "{user}, உன்னை வீடியோ காலுக்கு அழைச்சாங்க!",
    "{user}, என்னடா இவனுக்கு வீடியோ காலுக்கு அழைப்பு? 😅",
    "{user}, நேரம் போச்சு வீடியோ காலுக்கு வருடா!"
]

# Custom message when a user is invited to a video chat
@app.on_message(filters.group & filters.video_chat_started)
async def video_chat_invite(client: Client, message):
    if message.video_chat_participants_invited:
        invited_users = [user.first_name for user in message.video_chat_participants_invited.users]  # Get the invited users' first names
        for user in invited_users:
            response = random.choice(video_chat_responses).format(user=user)  # Choose a random response for each invited user
            await message.reply_text(response)