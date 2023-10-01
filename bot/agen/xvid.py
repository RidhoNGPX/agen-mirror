from bs4 import BeautifulSoup
import requests as req
from bot.helper.agenhelper.pyrohelper import get_arg
from bot import app
from pyrogram import filters



@app.on_message(filters.command("xvideos"))
async def xvid(_, message):
  query = get_arg(message)
  if not query:
    return await message.reply("Give something to search")
  url = f"https://www.xvideos.com/?k={query}"
  res = req.get(url).text
  soup = BeautifulSoup(res, "lxml")
  search_result = soup.find_all('div', class_='thumb-block')
  data = ""
  for entry in search_result:
        main = entry.p
        link =  "https://xvideos.com" + main.a['href']
        nj = main.a
        name = nj.attrs.get("title")
        data += f"[•{name}]({link})\n"
  data = f"**Search result for** `{query}`:\n{data}"
  await message.reply(text=data, disable_web_page_preview=True)
