from pyrogram import filters
from bot import app
from bot.helper.telegram_helper.bot_commands import BotCommands
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)









MIRRORHELP = """
/mirror: Start mirroring to Google Drive.
/zipmirror: Start mirroring and upload the file/folder compressed with zip extension 
/unzipmirror: Start mirroring and upload the file/folder extracted from any archive extension 
/qbmirror: Start Mirroring using qBittorrent 
/qbzipmirror: Start mirroring using qBittorrent and upload the file/folder compressed with zip extension 
/qbunzipmirror: Start mirroring using qBittorrent and upload the file/folder extracted from any archive extension
/watch: Mirror yt-dlp supported link
/zipwatch: Mirror yt-dlp supported link as zip 
"""

OTHERHELP = f"""
/clone: Copy file/folder to Google Drive
/count: Count file/folder of Google Drive 
/del: Delete file/folder from Google Drive (Only Owner & Sudo)
/cancel: Reply to the message by which the download was initiated and that download will be cancelled 
/cancelall: Cancel all downloading tasks 
/list: Search in Google Drive(s) 
/search: Search for torrents with API
/status: Shows a status of all the downloads 
/stats: Show Stats of the machine the bot is hosted on
/{BotCommands.PingCommand}: Check how long it takes to Ping the Bot
/{BotCommands.AuthorizeCommand}: Authorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)
/{BotCommands.UnAuthorizeCommand}: Unauthorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)
/{BotCommands.AuthorizedUsersCommand}: Show authorized users (Only Owner & Sudo)
/{BotCommands.AddSudoCommand}: Add sudo user (Only Owner)
/{BotCommands.RmSudoCommand}: Remove sudo users (Only Owner)
/{BotCommands.RestartCommand}: Restart and update the bot
/{BotCommands.LogCommand}: Get a log file of the bot. Handy for getting crash reports
/{BotCommands.ShellCommand}: Run commands in Shell (Only Owner)
/{BotCommands.ExecHelpCommand}: Get help for Executor module (Only Owner)
"""

LEECHHELP = """
/leech: Start leeching to Telegram
/zipleech: Start leeching to Telegram and upload the file/folder compressed with zip extension 
/unzipleech: Start leeching to Telegram and upload the file/folder extracted from any archive extension 
/qbleech: Start leeching to Telegram using qBittorrent
/qbzipleech: Start leeching to Telegram using qBittorrent and upload the file/folder compressed with zip extension 
/qbunzipleech: Start leeching to Telegram using qBittorrent and upload the file/folder extracted from any archive extension
/leechwatch: Leech yt-dlp supported link 
/leechzipwatch: Leech yt-dlp supported link as zip 
/leechset: Leech settings 
/setthumb: Reply photo to set it as thumbnail
"""

CUSTOMOD = """
/id: get chat_id/user_id/file_id
/genss : Generate screenshot from video
/bypass: To bypass supported url
/paste: Paste the text to the batbin website
/mediainfo : Get Media Details Info
/xvideos: Search videos from xvideos website
/stickerid: reply to a sticker to me to tell you its file ID.
/getsticker: reply to a sticker to me to upload its raw PNG file.
/kang: reply to a sticker to add it to your pack.
/stickers: Find stickers for given term on combot sticker catalogu 
"""



BUTTON = [[
            InlineKeyboardButton(text="Mirror Command", callback_data="mirror_"),
          ],
          [ InlineKeyboardButton(text="Leech Command", callback_data="leech_")
          ],
          [ InlineKeyboardButton(text="Other Command", callback_data="other_")
          ],
          [ InlineKeyboardButton(text="Custome Module", callback_data="cusmod_")
          ],
          [
            InlineKeyboardButton(text="Close", callback_data="close_")
          ]]
MARKUP = InlineKeyboardMarkup(BUTTON)



@app.on_message(filters.command("help"))
async def helep(_, message):
    HELPTEXT = f"""
Hello @{message.from_user.username}
This is a list of Agen Mirror bot menus.You can read the instructions via the button below
"""
    await message.reply(text=HELPTEXT, reply_markup=MARKUP)


@app.on_callback_query(filters.regex(pattern=r"^mirror_"))
async def morehlp(_, cq: CallbackQuery):
    if (cq.from_user.id == cq.message.reply_to_message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Back", callback_data="home_")]]
        )
        await cq.message.edit(text=MIRRORHELP, reply_markup=keyboard)
    else:
        await cq.answer("Not your requests", show_alert=True)


@app.on_callback_query(filters.regex(pattern=r"^leech_"))
async def extrhlp(_, cq: CallbackQuery):
    if (cq.from_user.id == cq.message.reply_to_message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Back", callback_data="home_")]]
        )
        await cq.message.edit(text=LEECHHELP, reply_markup=keyboard)
    else:
        await cq.answer("Not your requests", show_alert=True)


@app.on_callback_query(filters.regex(pattern=r"^other_"))
async def extrhlp(_, cq: CallbackQuery):
    if (cq.from_user.id == cq.message.reply_to_message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Back", callback_data="home_")]]
        )
        await cq.message.edit(text=OTHERHELP, reply_markup=keyboard)
    else:
        await cq.answer("Not your requests", show_alert=True)


@app.on_callback_query(filters.regex(pattern=r"^cusmod_"))
async def extrhlp(_, cq: CallbackQuery):
    if (cq.from_user.id == cq.message.reply_to_message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Back", callback_data="home_")]]
        )
        await cq.message.edit(text=CUSTOMOD, reply_markup=keyboard)
    else:
        await cq.answer("Not your requests", show_alert=True)



@app.on_callback_query(filters.regex(pattern=r"home_"))
async def homehlp(_, cq: CallbackQuery):
    HOMETEXT = f"""
Hello @{cq.from_user.username}
This is a list of Agen Mirror bot menus.You can read the instructions via the button below
"""
    if (cq.from_user.id == cq.message.reply_to_message.from_user.id):
        await cq.message.edit(text=HOMETEXT, reply_markup=MARKUP)
    else:
        await cq.answer("Not your requests", show_alert=True)


@app.on_callback_query(filters.regex(pattern=r"close_"))
async def tutp(_, cq: CallbackQuery):
    if (cq.from_user.id == cq.message.reply_to_message.from_user.id):
        await cq.message.delete()
    else:
        await cq.answer("Not your requests", show_alert=True)
