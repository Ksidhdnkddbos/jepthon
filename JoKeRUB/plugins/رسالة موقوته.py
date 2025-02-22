from asyncio import sleep
from JoKeRUB import l313l
from JoKeRUB.core.logger import logging

plugin_category = "tools"
LOGS = logging.getLogger(__name__)

@l313l.ar_cmd(
    pattern="مؤقت (\d*) ([\s\S]*)",
    command=("مؤقت", plugin_category),
    info={
        "شـرح": "لأرسـال رسـالة موقوتة وحـذفها بعـد وقت معيـن انت تضعـه",
        "⌔︙أسـتخدام": "{tr}مؤقت [الوقت] [النص]",
        "᯽︙ امثـلة": "{tr}مؤقت 10 ههلا",
    },
)
async def selfdestruct(destroy):
    "᯽︙ لأرسـال رسـالة مـوقوتة"
    cat = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, message)
    await sleep(ttl)
    await smsg.delete()

@l313l.ar_cmd(
    pattern="حذف الكل (\d*)",
    command=("حذف الكل", plugin_category),
    info={
        "شـرح": "لحذف جميع الرسائل التي ترسلها بعد فترة زمنية محددة",
        "⌔︙أسـتخدام": "{tr}حذف الكل [الوقت]",
        "᯽︙ امثـلة": "{tr}حذف الكل 10",
    },
)
async def delete_all_messages(event):
    "᯽︙ لحذف جميع الرسائل التي ترسلها بعد فترة زمنية محددة"
    ttl = int(event.pattern_match.group(1))
    await event.delete()
    
    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        await sleep(ttl)
        await message.delete()
