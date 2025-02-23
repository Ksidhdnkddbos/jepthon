from telethon import events
from telethon.tl.functions.messages import DeleteMessagesRequest
from JoKeRUB import l313l

# قاموس لتخزين عدد الصور في كل مجموعة
group_media_count = {}

@l313l.on(events.NewMessage(func=lambda e: e.is_group and e.photo))
async def handle_media(event):
    chat_id = event.chat_id

    # زيادة العداد إذا كانت الرسالة تحتوي على صورة
    if chat_id not in group_media_count:
        group_media_count[chat_id] = 0
    group_media_count[chat_id] += 1

    # إذا وصل عدد الصور إلى 25، قم بحذفها وإرسال إشعار
    if group_media_count[chat_id] >= 25:
        await delete_media(event)
        group_media_count[chat_id] = 0  # إعادة العداد إلى الصفر
        await event.reply("تم حذف 25 صورة تلقائيًا.")

async def delete_media(event):
    # حذف الرسائل التي تحتوي على صور
    messages_to_delete = []
    async for message in l313l.iter_messages(event.chat_id, limit=25):
        if message.photo:
            messages_to_delete.append(message.id)

    if messages_to_delete:
        await l313l(DeleteMessagesRequest(event.chat_id, messages_to_delete))
