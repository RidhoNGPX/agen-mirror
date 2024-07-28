# This scripts contains use cases for simple bots

import google.generativeai as genai
from bot import app
from pyrogram import Client, filters
from pyrogram.types import Message

API_KEY="AIzaSyC7_AEzbreEZPz1MAo1LusJxMSvarNudF8"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-pro")




@app.on_message(filters.command("tanya"))
async def say(app, message: Message):
    try:
        i = await message.reply_text(f"`Please Wait`")

        if len(message.command) > 1:
         prompt = message.text.split(maxsplit=1)[1]
        elif message.reply_to_message:
         prompt = message.reply_to_message.text
        else:
         await message.reply_text(
            f"Usage: `/ask [prompt/reply to message]`"
        )
         return
    
        chat = model.start_chat()
        response = chat.send_message(prompt)
        i.delete()
    
        await message.reply_text(f"**Question:**`{prompt}`\n**Answer:** {response.text}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")