
import re
import lk21
import json
from datetime import datetime
from urllib.parse import urlparse, unquote
from bot import app
from bot.helper.agenhelper.json_prettify import json_prettify
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.helper.agenhelper.pyrohelper import get_arg
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException
import cloudscraper
import base64

import requests
from bs4 import BeautifulSoup


fmed_list = ['fembed.net', 'cumpletlyaws.my.id', '2anakkb.my.id', 'cloudrls.com', 'fembed.com', 'fembad.org', 'henkasuru.my.id', 'femax20.com', 'fcdn.stream', 'feurl.com', 'naniplay.nanime.in', 'naniplay.nanime.biz', 'naniplay.com', 'layarkacaxxi.icu', 'dutrag.com', '2anakkb.my.id',
             'mrdhan.com', 'mm9842.com', 'diasfem.com', 'mycloudzz.com', 'asianclub.tv', 'iframe1videos.xyz', 'iframejav.net', 'watchjavnow.xyz', 'kotakajair.xyz', 'suzihaza.com', 'javsubs91.com', 'youtnbe.xyz', 'nekolink.site',
             '2tazhfx9vrx4jnvaxt87sknw5eqbd6as.club', 'watch-jav-english.live', 'streamabc.xyz', 'ns21.online', 'dbfilm.bar', 'panenjamu.xyz', 'gdplayer.xyz', 'play.dubindo.site', 'lk12.my.id', 
             'komikhentai.eu.org', 'tpxanime.in', 'javlove.club', 'pusatporn.live', 'anime789.com', '24hd.club', 'vcdn.io', 'sharinglink.club', 'votrefiles.club', 'femoload.xyz', 'dailyplanet.pw', 'jplayer.net',
             'xstreamcdn.com', 'gcloud.live', 'vcdnplay.com', 'vidohd.com', 'vidsource.me', 'votrefile.xyz', 'vanfem.com', 'zidiplay.com', 'mediashore.org', 'there.to', 'sexhd.co', 'viplayer.cc', 'votrefilms.xyz', 'embedsito.com',
             'youvideos.ru', 'streamm4u.club', 'moviepl.xyz', 'vidcloud.fun', 'fplayer.info', 'moviemaniac.org', 'albavido.xyz', 'ncdnstm.com', 'fembed-hd.com', 'superplayxyz.club', 'cinegrabber.com', 'savefilm21info.xyz', 'drama.xyz',
             'javstream.top', 'javpoll.com', 'ezsubz.com', 'reeoov.tube', 'diampokusy.com', 'vid21.vip']



@app.on_message(filters.command("bypass"))
async def direct_(app, message):
    """direct links generator"""
    text = get_arg(message)
    if not text:
        url = "https://telegra.ph/Robot-Gledek-05-07"
        tombol = [[
                InlineKeyboardButton('Fembed list', url=url),                
            ]]
        reply_markup = InlineKeyboardMarkup(tombol)
        teks = "**Gunakan** `/bypass [link]`\n\n**Supported Url**:\n**ouo - androidfilehost - fembed - streamtape - Yandisk - an1 - adfly - lendrive - linkvertise - psa**"
        await message.reply_text(text=teks, reply_markup=reply_markup)
        return
    links = re.findall(r"\bhttps?://.*\.\S+", text)
    if not links:
        await message.reply("`Use /bypass url`")
        return
    k = await message.reply("`Processing...`")
    for link in links:
        if "ouo.press" in link:
            reply = f"{ouo_bypass(link)}\n"
        elif "ouo.io" in link:
            reply = f"{ouo_bypass(link)}\n"
        elif "adf.ly" in link:
            reply = f"{adfly(link)}\n"
        elif "psa.pm" in link:
            reply = f"{psa_bypasser(link)}\n"
        elif "linkvertise.com" in link:
            reply = f"{linkvertise(link)}\n"
        elif "an1.com" in link:
            reply = f"{an1(link)}\n"
        elif "androidfilehost.com" in link:
            reply = f"{androidfilehost(link)}\n"
        elif "streamtape.com" in link:
            reply = f"{streamtape(link)}\n"
        elif "strtape.cloud" in link:
            reply = f"{streamtape(link)}\n"
        elif "yadi.sk" in link:
            reply = f"{yandex_disk(link)}\n"
        elif "disk.yandex.com" in link:
            reply = f"{yandex_disk(link)}\n"
        elif "disk.yandex.ru" in link:
            reply = f"{yandex_disk(link)}\n"
        elif "lendrive.web.id" in link:
            reply = f"{lendrive(link)}\n"
        elif any(x in link for x in fmed_list):
            reply = f"{fembed(link)}\n"
        else:
            reply = f"**--Original Links--**:\n`{link}`\n\n**Url Not Supported**\n"
    await k.edit(reply, disable_web_page_preview=True)




def RecaptchaV3(ANCHOR_URL):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer

ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'



def ouo_bypass(url):
    s = datetime.now()
    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    
    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):
        
        if res.headers.get('Location'):
            break
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        
        ans = RecaptchaV3(ANCHOR_URL)
        data['x-token'] = ans
        
        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        
        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"
        e = datetime.now()
        ms = (e - s).seconds
        kuntul = f"**--Original Links--**:\n`{url}`\n\n**--Direct Links--:**\n`{res.headers.get('Location')}`\n\n**Elpased : **{ms}s"
    return kuntul



def fembed(link: str) -> str:
    s = datetime.now()
    bypasser = lk21.Bypass()
    dl_url = bypasser.bypass_fembed(link)
    data = json_prettify(dl_url)
    e = datetime.now()
    ms = (e - s).seconds
    jmbt = f"**--Original Links--**:\n`{link}`\n\n**--Direct Links--:**\n{data} \n\n**Mirror atau leech harus dengan bot yang sama saat bypass**\n\n**Elpased :** {ms}s"
    return jmbt
    


def streamtape(url: str) -> str:
    s = datetime.now()
    bypasser = lk21.Bypass()
    pler = bypasser.bypass_streamtape(url)
    e = datetime.now()
    ms = (e - s).seconds
    pukon = f"**--Original Links--**:\n`{url}`\n\n**--Direct Links--:**\n`{pler}`\n\n**Mirror atau leech harus dengan bot yang sama saat bypass**\n\n**Elpased** : {ms}s"
    return pukon






def yandex_disk(url: str) -> str:
    """ Yandex.Disk direct link generator
    Based on https://github.com/wldhx/yadisk-direct """
    try:
        s = datetime.now()
        link = re.findall(r'\b(https?://(yadi.sk|disk.yandex.com|disk.yandex.ru)\S+)', url)[0][0]
    except IndexError:
        return "No Yandex.Disk links found\n"
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        req = requests.get(api.format(link)).json()['href']
        e = datetime.now()
        ms = (e - s).seconds
        pkob =  f"**--Original Links--**:\n`{url}`\n\n**--Direct Links--:**\n`{req}`\n\n**Elpased :** {ms}s"
        return pkob
    except KeyError:
        raise DirectDownloadLinkException("ERROR: File tidak ditemukan/Batas unduhan tercapai\n")



def androidfilehost(url: str) -> str:
    """AFH direct links generator"""
    try:
        link = re.findall(r"\bhttps?://.*androidfilehost.*fid.*\S+", url)[0]
    except IndexError:
        reply = "`No AFH links found`\n"
        return reply
    s = datetime.now()
    fid = re.findall(r"\?fid=(.*)", link)[0]
    session = requests.Session()
    headers = {"user-agent": "Mozilla/5.0 (Linux; Android 5.1; vivo Y31 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        "origin": "https://androidfilehost.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Linux; Android 5.1; vivo Y31 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-mod-sbb-ctype": "xhr",
        "accept": "*/*",
        "referer": f"https://androidfilehost.com/?fid={fid}",
        "authority": "androidfilehost.com",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {"submit": "submit", "action": "getdownloadmirrors", "fid": f"{fid}"}
    mirrors = None
    reply = ""
    error = "`Error: Can't find Mirrors for the link`\n"
    try:
        req = session.post(
            "https://androidfilehost.com/libs/otf/mirrors.otf.php",
            headers=headers,
            data=data,
            cookies=res.cookies,
        )
        mirrors = req.json()["MIRRORS"]
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item["name"]
        dl_url = item["url"]
        e = datetime.now()
        ms = (e - s).seconds
        reply += f"•[{name}]({dl_url})\n"
    reply = f"**--Original Links--**:\n`{url}`\n\n**--Direct Links--:**\n{reply}\n**Elpased**: {ms} s"
    return reply


def lendrive(url: str) -> str:
    s = datetime.now()
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    result = soup.findAll("div", class_="soraurlx")
    e = datetime.now()
    ms = (e - s).seconds
    reply = f"**--Original Links--**:\n`{url}`\n\n**--Direct Links--:**\n{result}\n\n**Elpased**: {ms} s"
    return reply


def an1(url: str) -> str:
    s = datetime.now()
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    result = soup.findAll("a", class_="btn btn-lg btn-green")
    e = datetime.now()
    ms = (e - s).seconds
    reply = f"**--Original Links--**:\n`{url}`\n\n**--Direct Links--:**\n{result}\n\n**Elpased**: {ms} s"
    return reply


def decrypt_url(code):
    a, b = '', ''
    for i in range(0, len(code)):
        if i % 2 == 0: a += code[i]
        else: b = code[i] + b
    key = list(a + b)
    i = 0
    while i < len(key):
        if key[i].isdigit():
            for j in range(i+1,len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10: key[i] = str(u)
                    i = j					
                    break
        i+=1
    key = ''.join(key)
    decrypted = base64.b64decode(key)[16:-16]
    return decrypted.decode('utf-8')



def adfly(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    res = client.get(url).text
    link = url
    try:
        ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out['error'] = True
        return out
    url = decrypt_url(ysmm)
    if re.search(r'go\.php\?u\=', url):
        url = base64.b64decode(re.sub(r'(.*?)u=', '', url)).decode()
    elif '&dest=' in url:
        url = unquote(re.sub(r'(.*?)dest=', '', url))
    result = f"**--Original Links--**:\n`{link}`\n\n**--Direct Links--:**\n`{url}`"
    return result


