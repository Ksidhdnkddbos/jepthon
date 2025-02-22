from telethon import events
import asyncio

@l313l.on(events.NewMessage(pattern="(تدمير|ذاتية التدمير)"))
async def self_destruct(event):
    # استخراج الوقت من الرسالة (بالثواني)
    try:
        # افتراضيًا، إذا لم يتم تحديد الوقت، سيتم تعيينه إلى 10 ثواني
        time_to_delete = int(event.text.split(" ")[1]) if len(event.text.split(" ")) > 1 else 10
    except ValueError:
        await event.reply("**᯽︙ الوقت يجب أن يكون رقمًا!**")
        return

    # إرسال رسالة تأكيد
    message = await event.reply(f"**᯽︙ هذه الرسالة ستحذف بعد {time_to_delete} ثانية...**")

    # انتظار الوقت المحدد
    await asyncio.sleep(time_to_delete)

    # حذف الرسالة
    await message.delete()
