from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import os
import datetime
from telethon import events
from JoKeRUB import *

Aljoker_Asbo3 = {
    'Monday': 'الاثنين',
    'Tuesday': 'الثلاثاء',
    'Wednesday': 'الأربعاء',
    'Thursday': 'الخميس',
    'Friday': 'الجمعة',
    'Saturday': 'السبت',
    'Sunday': 'الأحد'
}

@l313l.on(admin_cmd(pattern="(جلب الصورة|جلب الصوره|ذاتيه|ذاتية)"))
async def dato(event):
    if not event.is_reply:
        return await event.edit("..")
    lMl10l = await event.get_reply_message()
    pic = await lMl10l.download_media()
    await bot.send_file(
        "me",
        pic,
        caption=f"""
- تـم حفظ الصـورة بنجـاح ✓ 
- غير مبري الذمه اذا استخدمت الامر للابتزاز
- CH: @aghvv
- Dev: @lx5x5
  """,
    )
    await event.delete()

@l313l.on(admin_cmd(pattern="(الذاتية تشغيل|ذاتية تشغيل)"))
async def reda(event):
    if gvarstatus("savepicforme"):
        return await edit_delete(event, "**᯽︙حفظ الذاتيات مفعل وليس بحاجة للتفعيل مجدداً **")
    else:
        addgvar("savepicforme", "reda")
        await edit_delete(event, "**᯽︙تم تفعيل ميزة حفظ الذاتيات بنجاح ✓**")

@l313l.on(admin_cmd(pattern="(الذاتية تعطيل|ذاتية تعطيل)"))
async def Reda_Is_Here(event):
    if gvarstatus("savepicforme"):
        delgvar("savepicforme")
        return await edit_delete(event, "**᯽︙تم تعطيل حفظت الذاتيات بنجاح ✓**")
    else:
        await edit_delete(event, "**᯽︙انت لم تفعل حفظ الذاتيات لتعطيلها!**")

def joker_unread_media(message):
    return message.media_unread and (message.photo or message.video)

async def Hussein(event, caption):
    media = await event.download_media()
    sender = await event.get_sender()
    sender_id = event.sender_id
    lMl10l_date = event.date.strftime("%Y-%m-%d")
    lMl10l_day = Aljoker_Asbo3[event.date.strftime("%A")]
    await bot.send_file(
        "me",
        media,
        caption=caption.format(sender.first_name, sender_id, lMl10l_date, lMl10l_day),
        parse_mode="markdown"
    )
    os.remove(media)

@l313l.on(events.NewMessage(func=lambda e: e.is_private and joker_unread_media(e) and e.sender_id != bot.uid))
async def Reda(event):
    if gvarstatus("savepicforme"):
        caption = """**
           ♡  غير مبري الذمة اذا استعملته للأبتزاز  ♡
♡ تم حفظ الذاتية بنجاح ✓
♡ تم الصنع : @lx5x5
♡ أسم المرسل : [{0}](tg://user?id={1})
♡  تاريخ الذاتية : `{2}`
♡  أرسلت في يوم `{3}`
       ♡    Karar    ♡
        **"""
        await Hussein(event, caption)

@l313l.on(admin_cmd(pattern="نقطتين"))
async def read_selfie(event):
    if not event.is_reply:
        return  # لا تقم بأي شيء إذا لم يتم الرد على رسالة
    
    replied_message = await event.get_reply_message()
    
    # التحقق من أن الرسالة التي تم الرد عليها تحتوي على صورة أو فيديو
    if replied_message.photo or replied_message.video:
        try:
            await replied_message.mark_read()  # تمييز الرسالة كمقروءة
        except Exception as e:
            print(f"حدث خطأ أثناء محاولة قراءة الذاتية: {e}")
