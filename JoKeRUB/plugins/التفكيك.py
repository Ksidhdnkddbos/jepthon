import asyncio
from telethon import events
from telethon.tl.types import Message
from ..core.managers import edit_or_reply
from ..helpers.utils import _catutils
from ..config import config 
from . import l313l
#كرار
def split_arabic(input_text):
    letters = []
    for char in input_text:
        if char.isalpha():
            letters.append(char)
    return ' '.join(letters)

@l313l.ar_cmd(pattern=f"ت(?: |$)(.*)")
async def handle_event(event):
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
        await l313l.send_message(event.chat_id, split_message)
        await event.delete()
    except Exception as e:
        print(f"حدث خطأ: {e}")
