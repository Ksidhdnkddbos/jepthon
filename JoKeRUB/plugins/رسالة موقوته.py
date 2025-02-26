from asyncio import sleep
from JoKeRUB import l313l
from JoKeRUB.core.logger import logging

plugin_category = "tools"
LOGS = logging.getLogger(__name__)

# متغير لتحديد ما إذا كان المسح التلقائي مفعلًا أم لا
auto_delete_enabled = False

@l313l.ar_cmd(
    pattern="تفعيل_المسح_التلقائي",
    command=("تفعيل_المسح_التلقائي", plugin_category),
    info={
        "شـرح": "لتـفعيل المسـح التلقـائي للرسـائل",
        "⌔︙أسـتخدام": "{tr}تفعيل_المسح_التلقائي",
    },
)
async def enable_auto_delete(event):
    "لتـفعيل المسـح التلقـائي للرسـائل"
    global auto_delete_enabled
    auto_delete_enabled = True
    await event.edit("**⌔︙ تم تفعيل المسح التلقائي للرسائل.**")

@l313l.ar_cmd(
    pattern="تعطيل_المسح_التلقائي",
    command=("تعطيل_المسح_التلقائي", plugin_category),
    info={
        "شـرح": "لتـعطيل المسـح التلقـائي للرسـائل",
        "⌔︙أسـتخدام": "{tr}تعطيل_المسح_التلقائي",
    },
)
async def disable_auto_delete(event):
    "لتـعطيل المسـح التلقـائي للرسـائل"
    global auto_delete_enabled
    auto_delete_enabled = False
    await event.edit("**⌔︙ تم تعطيل المسح التلقائي للرسائل.**")

@l313l.ar_cmd(
    pattern="مؤقت (\d*) ([\s\S]*)",
    command=("مؤقت", plugin_category),
    info={
        "شـرح": "لأرسـال رسـالة وسـيتم حذفها بعـد وقت معيـن انت تضعـه",
        "⌔︙أسـتخدام": "{tr}مسح_تلقائي [الوقت] [النص]",
        "᯽︙ امثـلة": "{tr}مسح_تلقائي 10 ههلا",
    },
)
async def auto_delete_message(event):
    "لأرسـال رسـالة وسـيتم حذفها بعـد وقت معيـن"
    global auto_delete_enabled
    if not auto_delete_enabled:
        await event.edit("**⌔︙ المسح التلقائي غير مفعل. يرجى تفعيله أولاً.**")
        return
    
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    await event.delete()
    smsg = await event.client.send_message(event.chat_id, message)
    await sleep(ttl)
    await smsg.delete()

@l313l.ar_cmd(
    pattern="حذف_الرسائل_القديمة",
    command=("حذف_الرسائل_القديمة", plugin_category),
    info={
        "شـرح": "لحـذف جميع الرسـائل التي تم إرسالها بواسطة البوت",
        "⌔︙أسـتخدام": "{tr}حذف_الرسائل_القديمة",
    },
)
async def delete_old_messages(event):
    "لحـذف جميع الرسـائل التي تم إرسالها بواسطة البوت"
    await event.edit("**⌔︙ جاري حذف الرسائل القديمة...**")
    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        await message.delete()
        await sleep(1)  # لتجنب حظر الحساب بسبب كثرة الطلبات
    await event.edit("**⌔︙ تم حذف جميع الرسائل القديمة بنجاح.**")
