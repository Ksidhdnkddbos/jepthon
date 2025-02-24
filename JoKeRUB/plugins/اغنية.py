from telethon import events
from telethon.errors import ChatSendMediaForbiddenError
from youtube_search import YoutubeSearch
import yt_dlp
import requests
import os
import base64
from pathlib import Path
import urllib.parse

def get_cookies_file():
    folder_path = f"{os.getcwd()}/karar"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file

@l313l.ar_cmd(
    pattern="بحث(?: |$)(.*)",
    command=("بحث", plugin_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "usage": "{tr}بحث + اسم المقطع الصوتي",
        "examples": "{tr}بحث memories song",
    },
)
async def _(event):
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**⎉╎قم باضافـة إسـم للامـر ..**\n**⎉╎بحث + اسـم المقطـع الصـوتي**")
    
    catevent = await edit_or_reply(event, "**╮ جـارِ البحث ؏ـن المقطـٓع الصٓوتـي... 🎧♥️╰**")
    ydl_ops = {
        "format": "bestaudio[ext=m4a]",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
        "no_warnings": True,
    }
    
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        try:
            open(thumb_name, "wb").write(thumb.content)
        except Exception:
            thumb_name = None
            pass
        duration = results[0]["duration"]

    except Exception as e:
        await catevent.edit(f"**- فشـل التحميـل** \n**- الخطأ :** `{str(e)}`")
        await event.client.send_message(event.chat_id, "**- استخدم امر التحميل البديـل**\n**- ارسـل (.تحميل + اسم المقطع الصوتي)**")
        return
    
    await catevent.edit("**╮ جـارِ التحميل ▬▭ . . .🎧♥️╰**")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        host = str(info_dict["uploader"])
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await catevent.edit("**╮ جـارِ الرفـع ▬▬ . . .🎧♥️╰**")
        await event.client.send_file(
            event.chat_id,
            audio_file,
            force_document=False,
            caption=f"**⎉╎البحث :** `{title}`",
            thumb=thumb_name,
        )
        await catevent.delete()
    except ChatSendMediaForbiddenError as err:
        await catevent.edit("**- عـذراً .. الوسـائـط مغلقـه هنـا ؟!**")
        LOGS.error(str(err))
    except Exception as e:
        await catevent.edit(f"**- فشـل التحميـل** \n**- الخطأ :** `{str(e)}`")
        await event.client.send_message(event.chat_id, "**- استخدم امر التحميل البديـل**\n**- ارسـل (.تحميل + اسم المقطع الصوتي)**")
    try:
        os.remove(audio_file)
        if thumb_name:
            os.remove(thumb_name)
    except Exception as e:
        print(e)
