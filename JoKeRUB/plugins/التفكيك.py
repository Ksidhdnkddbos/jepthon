import asyncio
from telethon import events
from telethon.tl.types import Message
from JoKeRUB.core.managers import edit_or_reply
from JoKeRUB.helpers.utils import _catutils

# تعريف الوظيفة split_arabic
def split_arabic(text):
    return ' '.join(list(text))

@l313l.on(events.NewMessage(pattern=f"ت(?: |$)(.*)"))
async def break_word(event):
    try:
        malath = event.pattern_match.group(1)
        if malath:
            karar = malath
        elif event.is_reply:
            karar = await event.get_reply_message()
        else:
            return await edit_or_reply(event, "**⎉╎باضافة كلمة لـ الامـر او بالـࢪد ؏ــلى كلمة لتفكيكها**")
        
        # استدعاء الوظيفة split_arabic
        split_message = split_arabic(karar)
        await event.reply(split_message)  # الرد على الرسالة
        await event.delete()  # حذف الرسالة الأصلية
    except Exception as e:
        print(f"حدث خطأ: {e}")
