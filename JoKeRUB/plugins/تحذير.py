import html
from telethon import Button, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from JoKeRUB import l313l
from ..core.managers import edit_or_reply
from ..sql_helper import warns_sql as sql

plugin_category = "admin"

# --- الدوال الجديدة ---

async def mute_user(event, user_id, duration=None):
    """
    دالة لكتم المستخدم.
    - إذا تم تحديد المدة، يتم الكتم لمدة محددة.
    - إذا لم يتم تحديد المدة، يتم الكتم بشكل دائم.
    """
    try:
        if duration:
            await event.client.edit_permissions(
                event.chat_id,
                user_id,
                send_messages=False,
                until_date=duration,
            )
            await event.respond(f"تم كتم المستخدم لمدة {duration} ثانية.")
        else:
            await event.client.edit_permissions(
                event.chat_id,
                user_id,
                send_messages=False,
            )
            await event.respond("تم كتم المستخدم بشكل دائم.")
    except Exception as e:
        await event.respond(f"حدث خطأ أثناء محاولة كتم المستخدم: {e}")

async def restrict_user(event, user_id, duration=None):
    """
    دالة لتقييد المستخدم.
    - إذا تم تحديد المدة، يتم التقييد لمدة محددة.
    - إذا لم يتم تحديد المدة، يتم التقييد بشكل دائم.
    """
    try:
        if duration:
            await event.client.edit_permissions(
                event.chat_id,
                user_id,
                send_messages=False,
                until_date=duration,
            )
            await event.respond(f"تم تقييد المستخدم لمدة {duration} ثانية.")
        else:
            await event.client.edit_permissions(
                event.chat_id,
                user_id,
                send_messages=False,
            )
            await event.respond("تم تقييد المستخدم بشكل دائم.")
    except Exception as e:
        await event.respond(f"حدث خطأ أثناء محاولة تقييد المستخدم: {e}")

async def ban_user(event, user_id):
    """
    دالة لحظر المستخدم.
    """
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id,
                user_id,
                ChatBannedRights(until_date=None, view_messages=True),
            )
        )
        await event.respond("تم حظر المستخدم.")
    except Exception as e:
        await event.respond(f"حدث خطأ أثناء محاولة حظر المستخدم: {e}")

async def kick_user(event, user_id):
    """
    دالة لطرد المستخدم.
    """
    try:
        await event.client.kick_participant(event.chat_id, user_id)
        await event.respond("تم طرد المستخدم.")
    except Exception as e:
        await event.respond(f"حدث خطأ أثناء محاولة طرد المستخدم: {e}")

# --- دالة التحذير ---

@l313l.ar_cmd(
    pattern="تحذير(?:\s|$)([\s\S]*)",
    command=("تحذير", plugin_category),
    info={
        "header": "لتحذير المستخدم.",
        "description": "سيحذر المستخدم الذي تم الرد عليه.",
        "usage": "تحذير <السبب>",
    },
)
async def _(event):
    "لتحذير المستخدم"
    warn_reason = event.pattern_match.group(1)
    if not warn_reason:
        warn_reason = "- لا يوجد سبب ، 🗒"
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        str(reply_message.sender_id), event.chat_id, warn_reason
    )
    
    reply = "**▸┊[ المستخدم 👤](tg://user?id={}) **لديه {}/{} تحذيرات، احذر!**".format(
        reply_message.sender_id, num_warns, limit
    )
    if warn_reason:
        reply += "\n▸┊سبب التحذير الأخير \n{}".format(html.escape(warn_reason))
    
    await edit_or_reply(event, reply)

    # إرسال رسالة الأزرار عند وصول المستخدم إلى 3 تحذيرات
    if num_warns == 3:
        buttons = [
            [Button.inline("كتم", data="mute_user")],
            [Button.inline("تقييد", data="restrict_user")],
            [Button.inline("حظر", data="ban_user")],
            [Button.inline("طرد", data="kick_user")],
            [Button.inline("كتم 24 ساعة", data="mute_24h")],
            [Button.inline("تقييد 24 ساعة", data="restrict_24h")]
        ]
        await event.reply("**▸┊لقد وصل المستخدم إلى 3 تحذيرات، اختر الإجراء المناسب:**", buttons=buttons)

# --- دالة التعامل مع الأزرار ---

@l313l.on(events.CallbackQuery)
async def handle_button_click(event):
    # الحصول على بيانات الزر الذي تم النقر عليه
    data = event.data.decode("utf-8")
    
    # الحصول على المستخدم الذي تم الرد عليه
    reply_message = await event.get_message()
    user_id = reply_message.reply_to_msg_id  # يمكن تعديل هذا حسب الكود الخاص بك
    
    # التعامل مع الأزرار بناءً على البيانات
    if data == "mute_user":
        await mute_user(event, user_id)  # كتم دائم
    elif data == "restrict_user":
        await restrict_user(event, user_id)  # تقييد دائم
    elif data == "ban_user":
        await ban_user(event, user_id)  # حظر
    elif data == "kick_user":
        await kick_user(event, user_id)  # طرد
    elif data == "mute_24h":
        await mute_user(event, user_id, duration=86400)  # كتم لمدة 24 ساعة
    elif data == "restrict_24h":
        await restrict_user(event, user_id, duration=86400)  # تقييد لمدة 24 ساعة
    
    # تأكيد النقر على الزر
    await event.answer()
