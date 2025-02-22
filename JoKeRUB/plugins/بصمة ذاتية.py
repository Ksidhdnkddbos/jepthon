from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import os
import datetime
import asyncio
from telethon import events
from JoKeRUB import *

# أيام الأسبوع بالعربية
Aljoker_Asbo3 = {
    'Monday': 'الاثنين',
    'Tuesday': 'الثلاثاء',
    'Wednesday': 'الأربعاء',
    'Thursday': 'الخميس',
    'Friday': 'الجمعة',
    'Saturday': 'السبت',
    'Sunday': 'الأحد'
}

# أمر جلب الصوت
@l313l.on(admin_cmd(pattern="(جلب الصوت|جلب صوت|صوت)"))
async def dato(event):
    if not event.is_reply:
        return await event.edit("يجب الرد على رسالة صوتية لاستخدام هذا الأمر.")
    
    lMl10l = await event.get_reply_message()
    if not lMl10l.voice:
        return await event.edit("الرد يجب أن يكون على رسالة صوتية.")
    
    voice = await lMl10l.download_media(file="voices/")
    await bot.send_file(
        "me",  # إرسال الملف إليك
        voice,
        caption=f"""
- تـم حفظ الـصوت بنجـاح ✓ 
- غير مبري الذمه اذا استخدمت الامر للابتزاز
- CH: @Jepthon
- Dev: @lMl10l
  """,
    )

# تفعيل حفظ الرسائل الصوتية
@l313l.on(admin_cmd(pattern="(الصوت تشغيل|صوت تشغيل)"))
async def reda(event):
    if gvarstatus("savevoiceforme"):
        return await edit_delete(event, "**᯽︙حفظ الرسائل الصوتية مفعل وليس بحاجة للتفعيل مجدداً **")
    else:
        addgvar("savevoiceforme", "reda")
        await edit_delete(event, "**᯽︙تم تفعيل ميزة حفظ الرسائل الصوتية بنجاح ✓**")

# تعطيل حفظ الرسائل الصوتية
@l313l.on(admin_cmd(pattern="(الصوت تعطيل|صوت تعطيل)"))
async def Reda_Is_Here(event):
    if gvarstatus("savevoiceforme"):
        delgvar("savevoiceforme")
        return await edit_delete(event, "**᯽︙تم تعطيل حفظ الرسائل الصوتية بنجاح ✓**")
    else:
        await edit_delete(event, "**᯽︙انت لم تفعل حفظ الرسائل الصوتية لتعطيلها!**")

# دالة للتحقق من وجود رسالة صوتية
def joker_unread_voice(message):
    return message.media_unread and message.voice

# دالة لحفظ الرسائل الصوتية وإرسالها مع التدمير الذاتي
async def Hussein(event, caption):
    voice = await event.download_media(file="voices/")
    sender = await event.get_sender()
    sender_id = event.sender_id
    lMl10l_date = event.date.strftime("%Y-%m-%d")
    lMl10l_day = Aljoker_Asbo3[event.date.strftime("%A")]
    await bot.send_file(
        "me",
        voice,
        caption=caption.format(sender.first_name, sender_id, lMl10l_date, lMl10l_day),
        parse_mode="markdown"
    )

# حدث الاستماع للرسائل الصوتية الجديدة
@l313l.on(events.NewMessage(func=lambda e: e.is_private and joker_unread_voice(e) and e.sender_id != bot.uid))
async def Reda(event):
    if gvarstatus("savevoiceforme"):
        caption = """**
           ♡  غير مبري الذمة اذا استعملته للأبتزاز  ♡
♡ تم حفظ الرسالة الصوتية بنجاح ✓
♡ تم الصنع : @Jepthon
♡ أسم المرسل : [{0}](tg://user?id={1})
♡  تاريخ الرسالة : `{2}`
♡  أرسلت في يوم `{3}`
       ♡    ALJOKER    ♡
        **"""
        await Hussein(event, caption)
