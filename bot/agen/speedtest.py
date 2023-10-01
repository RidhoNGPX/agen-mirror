from speedtest import Speedtest
from bot import app
from pyrogram import filters
from bot.helper.agenhelper.custom_filters import agen_filter



@app.on_message(filters.command("speedtest") & agen_filter)
async def speedtest(_, message):
    speed = await message.reply("`Running Speed Test Please wait...`" )
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    string_speed = f"""
**SERVER :**
**Name :** `{result['server']['name']}`
**Country :** `{result['server']['country']}, {result['server']['cc']}`
**Sponsor :** `{result['server']['sponsor']}`
**ISP :** `{result['client']['isp']}`

**SPEEDTEST RESULTS : **
**Upload :** `{speed_convert(result['upload'] / 8)}`
**Download :**  `{speed_convert(result['download'] / 8)}`
**Ping :** `{result['ping']} ms`
**ISP Rating  :** `{result['client']['isprating']}`
"""
    await message.reply_photo(photo=path, caption=string_speed)
    await speed.delete()

def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "MB/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"
