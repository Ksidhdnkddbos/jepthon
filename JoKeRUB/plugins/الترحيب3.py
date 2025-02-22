from telethon import events
from telethon.utils import get_display_name
from JoKeRUB import l313l  # هذا هو الكائن الذي يمثل البوت الخاص بك
from JoKeRUB.core.logger import logging
from ..sql_helper.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

@l313l.on(events.ChatAction)
async def welcome_message(event):
    # التحقق من أن الحدث هو انضمام عضو جديد
    if event.user_joined or event.user_added:
        # الحصول على إعدادات الترحيب للمجموعة
        cws = get_current_welcome_settings(event.chat_id)
        if cws:
            # الحصول على معلومات العضو الجديد
            user = await event.get_user()
            if not user.bot:  # التأكد من أن العضو الجديد ليس بوتًا
                chat = await event.get_chat()
                title = get_display_name(chat) or "هذه المجموعة"
                mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
                first = user.first_name
                last = user.last_name
                fullname = f"{first} {last}" if last else first
                username = f"@{user.username}" if user.username else mention
                userid = user.id

                # تنسيق رسالة الترحيب
                welcome_message = cws.reply.format(
                    mention=mention,
                    title=title,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                )

                # إرسال رسالة الترحيب
                await event.reply(welcome_message, parse_mode="html")

@l313l.ar_cmd(
    pattern="ا ترحيب(?:\s|$)([\s\S]*)",
    command=("ا ترحيب", plugin_category),
    info={
        "header": "لحفظ رسالة ترحيب جديدة",
        "description": "يحفظ الرسالة كرسالة ترحيب للمجموعة.",
        "usage": "{tr}اضف ترحيب <رسالة الترحيب>",
        "examples": "{tr}اضف ترحيب مرحبًا {mention}، أنت العضو الجديد في {title}!",
    },
)
async def save_welcome(event):
    "لحفظ رسالة ترحيب جديدة"
    reply = await event.get_reply_message()
    text = "".join(event.text.split(maxsplit=1)[1:])
    if reply and not text:
        text = reply.text
    if not text:
        return await event.edit("**يرجى تقديم رسالة ترحيب!**")
    add_welcome_setting(event.chat_id, text)
    await event.edit("**تم حفظ رسالة الترحيب بنجاح!**")

@l313l.ar_cmd(
    pattern="ح_الترحيب$",
    command=("ح_الترحيب", plugin_category),
    info={
        "header": "لحذف رسالة الترحيب الحالية",
        "description": "يحذف رسالة الترحيب للمجموعة.",
        "usage": "{tr}حذف_الترحيب",
    },
)
async def delete_welcome(event):
    "لحذف رسالة الترحيب الحالية"
    if rm_welcome_setting(event.chat_id):
        await event.edit("**تم حذف رسالة الترحيب بنجاح!**")
    else:
        await event.edit("**لا توجد رسالة ترحيب محفوظة!**")

@l313l.ar_cmd(
    pattern="عرض_الترحيب$",
    command=("عرض_الترحيب", plugin_category),
    info={
        "header": "لعرض رسالة الترحيب الحالية",
        "description": "يعرض رسالة الترحيب المحفوظة للمجموعة.",
        "usage": "{tr}عرض_الترحيب",
    },
)
async def show_welcome(event):
    "لعرض رسالة الترحيب الحالية"
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        await event.edit(f"**رسالة الترحيب الحالية:**\n\n{cws.reply}")
    else:
        await event.edit("**لا توجد رسالة ترحيب محفوظة!**")
