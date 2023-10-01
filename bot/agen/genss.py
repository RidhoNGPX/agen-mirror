import os
import shutil
import time
import asyncio



from bot.helper.agenhelper import runcmd
from bot import app, DOWNLOAD_DIR
from pyrogram import filters
from bot.helper.agenhelper.progress import progress_for_pyrogram


@app.on_message(filters.command("genss"))
async def generate_screen_shot(app, message):
    replied = message.reply_to_message
    if not replied:
       await message.reply("reply to suported file")
       return
    if not (replied.video or replied.animation or (replied.document and "video" in replied.document.mime_type)):
       await message.reply("reply to video")
       return
    download_location = DOWNLOAD_DIR
    a = await message.reply(
        text="`Downloading Your Files...`"
    )
    c_time = time.time()
    the_real_download_location = await app.download_media(
        message=message.reply_to_message,
        file_name=download_location,
        progress=progress_for_pyrogram,
        progress_args=(
            "**Downloading Your Files...**",
            a,
            c_time
        )
    )
    await a.edit("`File Downloaded to {}`.".format(the_real_download_location))
    images = await runcmd(f'vcsi "{the_real_download_location}" -t -w 850 -g 3x5 --end-delay-percent 20 -o output.png')
    await a.edit(
        "`Now Uploading Your Files...`"
    )
    await message.reply_photo(photo="output.png", caption="**Screenshoot By :** @MirroringV3Bot\n**Powerded By :** [vcsi](https://pypi.org/project/vcsi/)")
    os.remove(the_real_download_location)
    await runcmd('rm output.png')
    await runcmd(f'rm -rf "{download_location}"')
    await runcmd('mkdir downloads')
    await a.delete()
