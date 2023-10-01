from re import findall as re_findall
from threading import Thread, Event
import calendar, time
from math import ceil
from html import escape
from psutil import virtual_memory, cpu_percent, disk_usage
from requests import head as rhead
from urllib.request import urlopen
from telegram import InlineKeyboardMarkup

from bot import download_dict, download_dict_lock, STATUS_LIMIT, botStartTime, DOWNLOAD_DIR
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker

MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"

COUNT = 0
PAGE_NO = 1


class MirrorStatus:
    STATUS_UPLOADING = "Uploading..."
    STATUS_DOWNLOADING = "Downloading..."
    STATUS_CLONING = "Cloning..."
    STATUS_WAITING = "Queued..."
    STATUS_PAUSE = "Paused..."
    STATUS_ARCHIVING = "Archiving..."
    STATUS_EXTRACTING = "Extracting..."
    STATUS_SPLITTING = "Splitting..."
    STATUS_CHECKING = "CheckingUp..."
    STATUS_SEEDING = "Seeding..."

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = Event()
        thread = Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

def getDownloadByGid(gid):
    with download_dict_lock:
        for dl in list(download_dict.values()):
            if dl.gid() == gid:
                return dl
    return None

def getAllDownload(req_status: str):
    with download_dict_lock:
        for dl in list(download_dict.values()):
            if dl:
                status = dl.status()
                if req_status == 'all':
                    return dl
                if req_status == 'down' and status in [MirrorStatus.STATUS_DOWNLOADING,
                                                         MirrorStatus.STATUS_WAITING,
                                                         MirrorStatus.STATUS_PAUSE]:
                    return dl
                if req_status == 'up' and status == MirrorStatus.STATUS_UPLOADING:
                    return dl
                if req_status == 'clone' and status == MirrorStatus.STATUS_CLONING:
                    return dl
                if req_status == 'seed' and status == MirrorStatus.STATUS_SEEDING:
                    return dl
                if req_status == 'split' and status == MirrorStatus.STATUS_SPLITTING:
                    return dl
                if req_status == 'extract' and status == MirrorStatus.STATUS_EXTRACTING:
                    return dl
                if req_status == 'archive' and status == MirrorStatus.STATUS_ARCHIVING:
                    return dl
    return None

def get_progress_bar_string(status):
    completed = status.processed_bytes() / 8
    total = status.size_raw() / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
    p_str = '▓' * cFull
    p_str += '░' * (12 - cFull)
    p_str = f"[{p_str}]"
    return p_str

def get_readable_message():
    with download_dict_lock:
        msg = ""
        ts = calendar.timegm(time.gmtime())
        if STATUS_LIMIT is not None:
            tasks = len(download_dict)
            global pages
            pages = ceil(tasks/STATUS_LIMIT)
            if PAGE_NO > pages and pages != 0:
                globals()['COUNT'] -= STATUS_LIMIT
                globals()['PAGE_NO'] -= 1
        for index, download in enumerate(list(download_dict.values())[COUNT:], start=1):
            msg += f"<b>Filename:</b> <code>{escape(str(download.name()))}</code>"
            msg += f"\n<b>Status:</b> <a href='{download.message.link}'>{download.status()}</a>"
            if download.status() not in [MirrorStatus.STATUS_SPLITTING, MirrorStatus.STATUS_SEEDING]:
                msg += f"\n{get_progress_bar_string(download)}↺<code>{download.progress()}</code>"
                if download.status() in [MirrorStatus.STATUS_DOWNLOADING,
                                         MirrorStatus.STATUS_WAITING,
                                         MirrorStatus.STATUS_PAUSE]:
                    msg += f"\n<b>Downloaded:</b> <code>{get_readable_file_size(download.processed_bytes())}</code> <b>of</b> <code>{download.size()}</code>"
                elif download.status() == MirrorStatus.STATUS_UPLOADING:
                    msg += f"\n<b>Uploaded:</b> <code>{get_readable_file_size(download.processed_bytes())}</code> <b>of</b> <code>{download.size()}</code>"
                elif download.status() == MirrorStatus.STATUS_CLONING:
                    msg += f"\n<b>Cloned:</b> <code>{get_readable_file_size(download.processed_bytes())}</code> <b>of</b> <code>{download.size()}</code>"
                elif download.status() == MirrorStatus.STATUS_ARCHIVING:
                    msg += f"\n<b>Archived:</b> <code>{get_readable_file_size(download.processed_bytes())}</code> <b>of</b> <code>{download.size()}</code>"
                elif download.status() == MirrorStatus.STATUS_EXTRACTING:
                    msg += f"\n<b>Extracted:</b> <code>{get_readable_file_size(download.processed_bytes())}</code> <b>of<b> <code>{download.size()}</code>"
                msg += f"\n<b>Speed:</b> <code>{download.speed()}</code> | <b>Eta:</b> <code>{download.eta()}</code>"
                try:
                    msg += f"\n<b>Seeders:</b> <code>{download.aria_download().num_seeders}</code>" \
                           f" | <b>Peers:</b> <code>{download.aria_download().connections}</code>"
                except:
                    pass
                try:
                    msg += f"\n<b>Seeders:</b> <code>{download.torrent_info().num_seeds}</code>" \
                           f" | <b>Leechers:</b> <code>{download.torrent_info().num_leechs}</code>"
                except:
                    pass
            elif download.status() == MirrorStatus.STATUS_SEEDING:
                msg += f"\n<b>Size: </b><code>{download.size()}</code>"
                msg += f"\n<b>Speed: </b><code>{get_readable_file_size(download.torrent_info().upspeed)}/s</code>"
                msg += f" | <b>Uploaded: </b><code>{get_readable_file_size(download.torrent_info().uploaded)}</code>"
                msg += f"\n<b>Ratio: </b><code>{round(download.torrent_info().ratio, 3)}</code>"
                msg += f" | <b>Time: </b><code>{get_readable_time(download.torrent_info().seeding_time)}</code>"
            else:
                msg += f"\n<b>Size: </b><code>{download.size()}</code>"
            msg += f"\n<b>Elpased:</b> <code>{get_readable_time(seconds=ts-int(download.message.date.timestamp()))}</code>"
            msg += f"\n<b>Machine:</b> {download.mesin()}"
            msg += f"\n<b>User:</b> @{download.message.from_user.username}(<code>{download.message.from_user.id}</code>)"
            msg += f"\n<b>To cancel</b>: <code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            msg += f"\n<b>_________________________________</b>"
            msg += "\n\n"
            if STATUS_LIMIT is not None and index == STATUS_LIMIT:
                break
        if len(msg) == 0:
            return None, None
        bmsg = f"<b>Cpu:</b> <code>{cpu_percent()}%</code> | <b>Ram:</b> <code>{virtual_memory().percent}%</code>"
        dlspeed_bytes = 0
        upspeed_bytes = 0
        for download in list(download_dict.values()):
            spd = download.speed()
            if download.status() == MirrorStatus.STATUS_DOWNLOADING:
                if 'K' in spd:
                    dlspeed_bytes += float(spd.split('K')[0]) * 1024
                elif 'M' in spd:
                    dlspeed_bytes += float(spd.split('M')[0]) * 1048576
            elif download.status() == MirrorStatus.STATUS_UPLOADING:
                if 'KB/s' in spd:
                    upspeed_bytes += float(spd.split('K')[0]) * 1024
                elif 'MB/s' in spd:
                    upspeed_bytes += float(spd.split('M')[0]) * 1048576
        bmsg += f"\n<b>▼:</b> {get_readable_file_size(dlspeed_bytes)}/s | <b>▲:</b> {get_readable_file_size(upspeed_bytes)}/s"
        if STATUS_LIMIT is not None and tasks > STATUS_LIMIT:
            msg += f"<b>Page:</b> {PAGE_NO}/{pages} | <b>Tasks:</b> {tasks}\n"
            buttons = ButtonMaker()
            buttons.sbutton("Previous", "status pre")
            buttons.sbutton("Next", "status nex")
            button = InlineKeyboardMarkup(buttons.build_menu(2))
            return msg + bmsg, button
        return msg + bmsg, ""

def turn(data):
    try:
        with download_dict_lock:
            global COUNT, PAGE_NO
            if data[1] == "nex":
                if PAGE_NO == pages:
                    COUNT = 0
                    PAGE_NO = 1
                else:
                    COUNT += STATUS_LIMIT
                    PAGE_NO += 1
            elif data[1] == "pre":
                if PAGE_NO == 1:
                    COUNT = STATUS_LIMIT * (pages - 1)
                    PAGE_NO = pages
                else:
                    COUNT -= STATUS_LIMIT
                    PAGE_NO -= 1
        return True
    except:
        return False

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def is_url(url: str):
    url = re_findall(URL_REGEX, url)
    return bool(url)

def is_gdrive_link(url: str):
    return "drive.google.com" in url

def is_mega_link(url: str):
    return "mega.nz" in url or "mega.co.nz" in url

def get_mega_link_type(url: str):
    if "folder" in url:
        return "folder"
    elif "file" in url:
        return "file"
    elif "/#F!" in url:
        return "folder"
    return "file"

def is_magnet(url: str):
    magnet = re_findall(MAGNET_REGEX, url)
    return bool(magnet)

def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper

def get_content_type(link: str) -> str:
    try:
        res = rhead(link, allow_redirects=True, timeout=5, headers = {'user-agent': 'Wget/1.12'})
        content_type = res.headers.get('content-type')
    except:
        try:
            res = urlopen(link, timeout=5)
            info = res.info()
            content_type = info.get_content_type()
        except:
            content_type = None
    return content_type
