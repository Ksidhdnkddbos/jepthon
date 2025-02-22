import re
from telethon.utils import get_display_name
from telethon.tl.types import DocumentAttributeSticker, DocumentAttributeAnimated
from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from ..sql_helper import blacklist_sql as sql
from ..utils import is_admin

plugin_category = "admin"

#copyright for JoKeRUB © 2021
@l313l.ar_cmd(incoming=True, groups_only=True)
async def on_new_message(event):
    # التحقق من أن الرسالة هي ملصق أو صورة متحركة
    if event.message.media:
        if hasattr(event.message.media, 'document'):
            attributes = event.message.media.document.attributes
            for attr in attributes:
                if isinstance(attr, DocumentAttributeSticker) or isinstance(attr, DocumentAttributeAnimated):
                    # الحصول على معرف الملف (File ID) للملصق أو الصورة المتحركة
                    file_id = event.message.media.document.id
                    # التحقق مما إذا كان المعرف موجودًا في قائمة المنع
                    if str(file_id) in sql.get_chat_blacklist(event.chat_id):
                        try:
                            await event.delete()
                            await event.reply("᯽︙ تم حذف الملصق/الصورة المتحركة لأنها محظورة.")
                        except Exception:
                            await event.client.send_message(
                                BOTLOG_CHATID,
                                f"᯽︙ ليـس لدي صـلاحيات الـحذف في {get_display_name(await event.get_chat())}.\
                                So removing blacklist stickers from this group",
                            )
                            for word in sql.get_chat_blacklist(event.chat_id):
                                sql.rm_from_blacklist(event.chat_id, word.lower())
                    break

    # المنطق الأصلي لمنع الكلمات
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    catadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not catadmin:
        return
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"᯽︙ ليـس لدي صـلاحيات الـحذف في {get_display_name(await event.get_chat())}.\
                     So removing blacklist words from this group",
                )
                for word in snips:
                    sql.rm_from_blacklist(event.chat_id, word.lower())
            break

@l313l.ar_cmd(
    pattern="منع(?:\s|$)([\s\S]*)",
    command=("منع", plugin_category),
    info={
        "header": "To add blacklist words or stickers to database",
        "description": "The given word or sticker ID will be added to blacklist in that specific chat if any user sends then the message gets deleted.",
        "note": "To block a sticker, reply to the sticker with the command `.منع`.",
        "usage": "{tr}addblacklist <word(s) or sticker>",
        "examples": ["{tr}addblacklist fuck", "{tr}addblacklist <sticker>"],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To add blacklist words or stickers to database"
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg.media:
            if hasattr(reply_msg.media, 'document'):
                attributes = reply_msg.media.document.attributes
                for attr in attributes:
                    if isinstance(attr, DocumentAttributeSticker) or isinstance(attr, DocumentAttributeAnimated):
                        file_id = reply_msg.media.document.id
                        sql.add_to_blacklist(event.chat_id, str(file_id))
                        await edit_or_reply(
                            event,
                            f"᯽︙ تم إضافة الملصق/الصورة المتحركة بقائمة المنع (ID: {file_id})."
                        )
                        return
    text = event.pattern_match.group(1)
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )

    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await edit_or_reply(
        event,
        "᯽︙ تم اضافة {} الكلمة في قائمة المنع بنجاح".format(
            len(to_blacklist)
        ),
    )

@l313l.ar_cmd(
    pattern="الغاء منع(?:\s|$)([\s\S]*)",
    command=("الغاء منع", plugin_category),
    info={
        "header": "To remove blacklist words or stickers from database",
        "description": "The given word or sticker ID will be removed from blacklist in that specific chat",
        "note": "To unblock a sticker, reply to the sticker with the command `.الغاء منع`.",
        "usage": "{tr}rmblacklist <word(s) or sticker>",
        "examples": ["{tr}rmblacklist fuck", "{tr}rmblacklist <sticker>"],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To Remove Blacklist Words or Stickers from Database."
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg.media:
            if hasattr(reply_msg.media, 'document'):
                attributes = reply_msg.media.document.attributes
                for attr in attributes:
                    if isinstance(attr, DocumentAttributeSticker) or isinstance(attr, DocumentAttributeAnimated):
                        file_id = reply_msg.media.document.id
                        if sql.rm_from_blacklist(event.chat_id, str(file_id)):
                            await edit_or_reply(
                                event,
                                f"᯽︙ تم إزالة الملصق/الصورة المتحركة من قائمة المنع (ID: {file_id})."
                            )
                        else:
                            await edit_or_reply(
                                event,
                                "᯽︙ الملصق/الصورة المتحركة غير موجودة في قائمة المنع."
                            )
                        return
    text = event.pattern_match.group(1)
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    successful = sum(
        bool(sql.rm_from_blacklist(event.chat_id, trigger.lower()))
        for trigger in to_unblacklist
    )
    await edit_or_reply(
        event, f"᯽︙ تم ازالة الكلمة {successful} / {len(to_unblacklist)} من قائمة المنع بنجاح"
    )

@l313l.ar_cmd(
    pattern="قائمة المنع$",
    command=("قائمة المنع", plugin_category),
    info={
        "header": "To show the blacklist words or stickers",
        "description": "Shows you the list of blacklist words or stickers in that specific chat",
        "usage": "{tr}listblacklist",
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To show the blacklist words or stickers in that specific chat"
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "᯽︙ قائمة المنع في الدردشة الحالية :\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👈 {trigger} \n"
    else:
        OUT_STR = " ᯽︙ لم تقم باضافة كلمات أو ملصقات سوداء. ارسل  `.منع` لمنع كلمة أو ملصق."
    await edit_or_reply(event, OUT_STR)
