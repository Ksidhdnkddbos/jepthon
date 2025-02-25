import os
import random
import string
from datetime import datetime

from PIL import Image
from telethon.utils import get_display_name
import requests  # إضافة مكتبة requests

from JoKeRUB import l313l

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "utils"


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


def upload_to_catbox(file_path):
    """
    رفع الملف إلى catbox.moe وإرجاع الرابط.
    """
    url = "https://catbox.moe/user/api.php"
    try:
        with open(file_path, "rb") as file:
            files = {"fileToUpload": file}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except Exception as e:
        LOGS.error(f"حدث خطأ أثناء الرفع إلى catbox.moe: {e}")
        return None


@l313l.ar_cmd(
    pattern="(ت(ل)?ك(راف)?) ?(m|t|ميديا|نص)(?:\s|$)([\s\S]*)",
    command=("تلكراف", plugin_category),
    info={
        "header": "To get catbox link.",
        "description": "Reply to text message to paste that text on catbox you can also pass input along with command \
            So that to customize title of that catbox and reply to media file to get sharable link of that media(atmost 5mb is supported)",
        "options": {
            "m or media": "To get catbox link of replied sticker/image/video/gif.",
            "t or text": "To get catbox link of replied text you can use custom title.",
        },
        "usage": [
            "{tr}tgm",
            "{tr}tgt <title(optional)>",
            "{tr}catbox media",
            "{tr}catbox text <title(optional)>",
        ],
    },
)
async def _(event):
    "To get catbox link."
    jokevent = await edit_or_reply(event, "` ⌔︙جـار انشـاء رابـط catbox`")
    optional_title = event.pattern_match.group(5)
    if not event.reply_to_msg_id:
        return await jokevent.edit(
            "` ⌔︙قـم بالـرد عـلى هـذه الرسـالة للحـصول عـلى رابـط catbox فـورا`",
        )

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()

    if input_str in ["ميديا", "m"]:
        try:
            # تحميل الملف
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await jokevent.edit(f"` ⌔︙تـم التحـميل الـى {downloaded_file_name}`")

            # إذا كان الملف من نوع .webp، نقوم بتحويله
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)

            # رفع الملف إلى catbox.moe
            file_url = upload_to_catbox(downloaded_file_name)
            if not file_url:
                await jokevent.edit("** ⌔︙خـطأ : **\n`فشل في رفع الملف إلى catbox.moe`")
                os.remove(downloaded_file_name)
                return

            # حساب الوقت المستغرق
            end = datetime.now()
            ms = (end - start).seconds

            # إرسال الرابط
            await jokevent.edit(
                f"** ⌔︙الـرابـط : **[إضـغط هنـا]({file_url})\
                    \n** ⌔︙الوقـت المأخـوذ : **`{ms} ثـانيـة.`",
                link_preview=False,
            )

            # حذف الملف المؤقت
            os.remove(downloaded_file_name)

        except Exception as e:
            await jokevent.edit(f"** ⌔︙حـدث خـطأ : **\n`{str(e)}`")
            if os.path.exists(downloaded_file_name):
                os.remove(downloaded_file_name)

    elif input_str in ["نص", "t"]:
        user_object = await event.client.get_entity(r_message.sender_id)
        title_of_page = get_display_name(user_object)
        # apparently, all Users do not have last_name field
        if optional_title:
            title_of_page = optional_title
        page_content = r_message.message
        if r_message.media:
            if page_content != "":
                title_of_page = page_content
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TEMP_DIR
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            for m in m_list:
                page_content += m.decode("UTF-8") + "\n"
            os.remove(downloaded_file_name)
        page_content = page_content.replace("\n", "<br>")
        try:
            # رفع النص إلى catbox.moe
            file_url = upload_to_catbox(downloaded_file_name)
            if not file_url:
                await jokevent.edit("** ⌔︙خـطأ : **\n`فشل في رفع الملف إلى catbox.moe`")
                return

            end = datetime.now()
            ms = (end - start).seconds
            await jokevent.edit(
                f"** ⌔︙الـرابـط : ** [اضغـط هنـا]({file_url})\
                     \n** ⌔︙الـوقـت المـأخـوذ : **`{ms} ثـانيـة.`",
                link_preview=False,
            )
        except Exception as e:
            LOGS.info(e)
            await jokevent.edit(f"** ⌔︙حـدث خـطأ : **\n`{str(e)}`")
