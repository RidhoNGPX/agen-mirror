import subprocess
from bot import app
from pyrogram import filters
from bot.helper.agenhelper.custom_filters import agen_filter
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery



@app.on_message(filters.command("log") & agen_filter)
async def semdlog(_, message):
    text = "Select the following for the option to send a log"
    BUTTON = [[
                InlineKeyboardButton(text="Send to Chanell", callback_data="tocenel_")
               ],
               [
                InlineKeyboardButton(text="Send as File", callback_data="send_"),
              ]]
    MARKUP = InlineKeyboardMarkup(BUTTON)
    await message.reply(text=text, reply_markup=MARKUP)


@app.on_callback_query(filters.regex(pattern=r"send_"))
async def logfile(_, c_q: CallbackQuery):
  if (c_q.from_user.id == c_q.message.reply_to_message.from_user.id):
    x = subprocess.getoutput("tail log.txt")
    filename = "log.txt"
    with open(filename, "w+", encoding="utf8") as out_file:
      out_file.write(str(x))
    await app.send_document(document=filename, chat_id=c_q.message.chat.id, reply_to_message_id=c_q.message.reply_to_message.id)
    await c_q.message.delete()
  else:
    await c_q.answer("You are not Agen", show_alert=True) 

@app.on_callback_query(filters.regex(pattern=r"tocenel_"))
async def logcenel(_, c_q: CallbackQuery):
  if (c_q.from_user.id == c_q.message.reply_to_message.from_user.id):
    x = subprocess.getoutput("tail log.txt")
    cenel = -1001646962211
    log = f"#BOTLOG\n{x}\n\n@MirroringV3bot"
    await app.send_message(text=log, chat_id=cenel, disable_web_page_preview=True)
    await c_q.message.edit("Succesfully Send to Log Channel")
  else:
    await c_q.answer("You are not Agen", show_alert=True) 
    
    
