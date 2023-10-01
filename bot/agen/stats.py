from bot import app, botStartTime
from pyrogram import filters
import shutil, psutil
from psutil import boot_time
import platform
import time
import requests as req
import json
import subprocess
from subprocess import check_output
import os
from os import path as ospath
from datetime import datetime
from bot.helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from bot.helper.agenhelper.neoimage import neo_image
from bot.helper.agenhelper.progress import progress_bar
from bot.agen import __all__ as modules
from platform import python_version
from pyrogram import __version__ as ve
from telegram import __version__ as o
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)



BUTTON = [[
            InlineKeyboardButton(text="IP", callback_data="_ip"),
           ],
           [
            InlineKeyboardButton(text="close", callback_data="close_"),
          ]]
MARKUP = InlineKeyboardMarkup(BUTTON)



@app.on_message(filters.command("stats"))
async def sys(app, message):
    agen = await message.reply("`Processing...`")
    if ospath.exists('.git'):
       last_commit = check_output(["git log -1 --date=short --pretty=format:'%cd <b>From</b> %cr'"], shell=True).decode()
    else:
        last_commit = 'No UPSTREAM_REPO'
    currentTime = get_readable_time(time.time() - botStartTime)
    osUptime = get_readable_time(time.time() - boot_time())
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent()
    disk = psutil.disk_usage('/').percent
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    memory = psutil.virtual_memory()
    mem_k = memory.percent
    mem_t = get_readable_file_size(memory.total)
    mem_a = get_readable_file_size(memory.available)
    mem_u = get_readable_file_size(memory.used)
    swap = psutil.swap_memory()
    swap_p = swap.percent
    swap_t = get_readable_file_size(swap.total)
    swap_u = get_readable_file_size(swap.used)
    memory = psutil.virtual_memory()
    mem_p = memory.percent
    mem_t = get_readable_file_size(memory.total)
    mem_a = get_readable_file_size(memory.available)
    mem_u = get_readable_file_size(memory.used)
    modul = len(modules)
    pic = "https://telegra.ph/file/208bbc6444530d245c2fb.png"
    stats = f"""
**BOT INFORMATION**
`Uptime : {currentTime}`
`Osuptime : {osUptime}`
`Version : {last_commit}`
`Custom Modules : {modul} modules`\n
**BOT ENGINE**
`Python Version : {python_version()}`
`Pyrogram Version : {ve}`
`Python Telegram Bot : {o}`\n
**CPU**
{progress_bar(cpuUsage)} - `{cpuUsage}%`
`Physical Cores : {p_core}`
`Total Cores : {t_core}`\n
**STORAGE**
{progress_bar(disk)} - `{disk}%`
`Total : {total}`
`Used : {used}`
`Free : {free}`\n
**VIRTUAL MEMORY**
{progress_bar(mem_k)} - `{mem_k}%`
`Total : {mem_t}`
`Used : {mem_u}`
`Free : {mem_a}`\n
**SWAP MEMORY**
{progress_bar(swap_p)} - `{swap_p}%`
`Total : {swap_t}`
`used : {swap_u}\n`
**DATA USAGE**
`Download : {recv}`
`Upload : {sent}`
"""
    await message.reply_photo(photo=pic, caption=stats, reply_markup=MARKUP)
    await agen.delete()

@app.on_message(filters.command("ping"))
async def ping(app, message):
    start = datetime.now()
    m = await message.reply("`🏓Pong!`")
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await m.edit(f"**🏓Pong!**\n`{m_s} ms`")



@app.on_callback_query(filters.regex(pattern=r"_ip"))
async def botip(_, cq: CallbackQuery):
    if (cq.from_user.id == cq.message.reply_to_message.from_user.id):
        url = "http://ip-api.com/json/"
        data = req.get(url).json()
        IP = data['query']
        ISP = data['isp']
        Organisation = data['org']
        country = data['country']
        City = data['city']
        Region = data['region']
        Timezone = data['timezone']
        test = f"""
My IP: {IP}
ISP: {ISP}
Organisation: {Organisation}
Country: {country}
City: {City}
Region: {Region}
Time zone: {Timezone}
"""
        await cq.answer(text=test, show_alert=True)
    else:
        await cq.answer("Not your requests", show_alert=True)
        
        
        


@app.on_callback_query(filters.regex(pattern=r"close_"))
async def tutp(_, cq: CallbackQuery):
    if (cq.from_user.id == cq.message.reply_to_message.from_user.id):
        await cq.message.delete()
    else:
        await cq.answer("Not your requests", show_alert=True)
        
        
 
        
