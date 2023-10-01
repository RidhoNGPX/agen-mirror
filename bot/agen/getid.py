from pyrogram import filters
from bot import app


@app.on_message(filters.command("id"))
async def showid(app, message):
    _id = ""
    _id += f"**Chat ID**: `{message.chat.id}`\n"
    if message.reply_to_message:
        _id += f"**Replied User ID**: `{message.reply_to_message.from_user.id}`\n"
        _id += f"**Your ID**: `{message.from_user.id}`\n"
    else:
        _id += f"**Your ID**: `{message.from_user.id}`\n"
    await message.reply_text(_id, quote=True)
