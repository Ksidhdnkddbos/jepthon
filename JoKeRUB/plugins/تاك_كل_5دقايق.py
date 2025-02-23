# By Reda for JoKeRUB
# Tel: @lx5x5
from JoKeRUB import l313l
import asyncio
import time
import random
from ..core.managers import edit_or_reply
from telethon import events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

spam_chats = []
mention_in_progress = False

# قائمة الكليشات (يمكنك إضافة أو تعديل الكليشات هنا)
clips = [
    "هلاو 🌹",
    "نورت 🫡",
    "أهلاً وسهلاً 😊",
    "مرحباً 👋",
    "كيفك؟ 🤗",
    "شرفتنا 🫶",
    "تفضل يا بطل 🦸‍♂️",
    "أهلاً بالغالي 🫂",
]

@l313l.ar_cmd(pattern="منشن_كل_5دقايق(?:\s|$)([\s\S]*)")
async def menall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await edit_or_reply(event, "** ᯽︙ هذا الامر يستعمل للقنوات والمجموعات فقط !**")
    msg = event.pattern_match.group(1)
    if not msg:
        return await edit_or_reply(event, "** ᯽︙ ضع رسالة للمنشن اولاً**")
    is_admin = False
    try:
        partici_ = await l313l(GetParticipantRequest(
          event.chat_id,
          event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in l313l.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        # اختيار كليشة عشوائية من القائمة
        clip = random.choice(clips)
        usrtxt = f"{clip}\n[{usr.first_name}](tg://user?id={usr.id}) "
        await l313l.send_message(chat_id, usrtxt)
        await asyncio.sleep(10)  # انتظار 5 دقائق
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@l313l.ar_cmd(pattern="الغاء_منشن_كل_5دقايق")
async def ca_sp(event):
  if not event.chat_id in spam_chats:
    return await edit_or_reply(event, "** ᯽︙ 🤷🏻 لا يوجد منشن لألغائه**")
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await edit_or_reply(event, "** ᯽︙ تم الغاء المنشن بنجاح ✓**")
