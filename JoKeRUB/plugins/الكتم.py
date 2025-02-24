import base64
import asyncio
from datetime import datetime
from telethon import events
from telethon.errors import BadRequestError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from JoKeRUB import l313l

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

plugin_category = "admin"
joker_users = []
joker_mute = "https://telegra.ph/file/c5ef9550465a47845c626.jpg"
joker_unmute = "https://telegra.ph/file/e9473ddef0b58cdd7f9e7.jpg"
import os

file_path = 'AljokerMute.txt'

# تحميل القائمة عند بدء التشغيل
if os.path.isfile(file_path):
    with open(file_path, 'r') as file:
        muted_ids = set(file.read().splitlines())
else:
    muted_ids = set()
    open(file_path, 'w').close()

def save_muted_ids():
    with open(file_path, 'w') as file:
        file.write("\n".join(muted_ids))

def add_to_mute_list(user):
    muted_ids.add(str(user.id))
    save_muted_ids()

def remove_from_mute_list(user_id):
    muted_ids.discard(str(user_id))
    save_muted_ids()

#=================== الكـــــــــــــــتم  ===================  #
@l313l.ar_cmd(pattern=f"كتم(?:\s|$)([\s\S]*)")
async def mutejep(event):
    args = event.pattern_match.group(1).strip()
    user = None

    if args.isdigit():  # إذا كان الـ ID رقمًا
        user_id = int(args)
        try:
            user = await event.client(GetFullUserRequest(user_id))
        except Exception as e:
            return await event.edit(f"**- خطأ: لا يمكن العثور على المستخدم بالـ ID {user_id}**")
    else:
        return await event.edit("**- يرجى تقديم ID صحيح**")

    if not user:
        return await event.edit("**- لم يتم العثور على المستخدم**")

    # باقي الكود الخاص بالكتم
    try:
        mute(user.user.id, event.chat_id)
        add_to_mute_list(user.user)
    except Exception as e:
        return await event.edit(f"**- خطأ: {e}**")

    await event.client.send_file(
        event.chat_id,
        joker_mute,
        caption=f"**- المستخدم: {_format.mentionuser(user.user.first_name, user.user.id)} \n- تم كتمه بنجاح ✓**",
    )

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#كتــم_الخــاص\n"
                f"**- الشخـص  :** [{replied_user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        args = event.pattern_match.group(1).strip()
        user = None

        if event.reply_to_msg_id:
            replied_message = await event.get_reply_message()
            user = await event.client.get_entity(replied_message.from_id)
        elif args:
            try:
                user = await event.client.get_entity(args)
            except Exception as e:
                return await event.edit(f"**- خطــأ : **`{e}`")

        if not user:
            return await event.edit("**- يرجى تقديم المعرف أو اسم المستخدم، أو الرد على رسالة المستخدم**")

        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await edit_or_reply(event, "** أنـا لسـت مشـرف هنـا ؟!! .**")
        if user.id == l313l.uid:
            return await edit_or_reply(event, "**𖡛... . لمـاذا تࢪيـد كتم نفسـك؟  ...𖡛**")
        if user.id == 5427469031:
            return await edit_or_reply(event, "** دي . . لا يمڪنني كتـم مطـور السـورس  ╰**")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(event, "**عــذراً .. هـذا الشخـص مكتــوم سـابقــاً هنـا**")
        result = await event.client.get_permissions(event.chat_id, user.id)
        try:
            if result.participant.banned_rights.send_messages:
                return await edit_or_reply(event, "**عــذراً .. هـذا الشخـص مكتــوم سـابقــاً هنـا**")
        except AttributeError:
            pass
        except Exception as e:
            return await edit_or_reply(event, f"**- خطــأ : **`{e}`")
        try:
            mute(user.id, event.chat_id)
            add_to_mute_list(user)
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(event, "**- عــذراً .. ليـس لديـك صـلاحيـة حـذف الرسـائل هنـا**")
            elif "creator" not in vars(chat):
                return await edit_or_reply(event, "**- عــذراً .. ليـس لديـك صـلاحيـة حـذف الرسـائل هنـا**")
        except Exception as e:
            return await edit_or_reply(event, f"**- خطــأ : **`{e}`")
        reason = event.pattern_match.group(1).split(maxsplit=1)[1] if len(event.pattern_match.group(1).split(maxsplit=1)) > 1 else ""
        if reason:
            await event.client.send_file(
                event.chat_id,
                joker_mute,
                caption=f"**- المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**- تـم كتمـه بنجـاح ✓**\n\n**- السـبب :** {reason}",
            )
        else:
            await event.client.send_file(
                event.chat_id,
                joker_mute,
                caption=f"**- المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}  \n**- تـم كتمـه بنجـاح ✓**\n\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكــتم\n"
                f"**الشخـص :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**الدردشـه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )

@l313l.on(events.NewMessage)
async def handle_forwarded(event):
    if event.fwd_from and is_muted(event.sender_id, event.chat_id):
        await event.delete()

#=================== الغـــــــــــــاء الكـــــــــــــــتم  ===================  #

@l313l.ar_cmd(pattern=f"(الغاء الكتم|الغاء كتم)(?:\s|$)([\s\S]*)")
async def unmutejep(event):
    if event.is_private:
        replied_user = await event.client.get_entity(event.chat_id)
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit("**عــذراً .. هـذا الشخـص غيــر مكتــوم هنـا**")
        try:
            unmute(event.chat_id, event.chat_id)
            if str(replied_user.id) in muted_ids:
                remove_from_mute_list(replied_user.id)
        except Exception as e:
            await event.edit(f"**- خطــأ : **`{e}`")
        else:
            await event.client.send_file(
                event.chat_id,
                joker_unmute,
                caption="**- تـم الغــاء كتــم الشخـص هنـا .. بنجــاح ✓**",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغــاء_الكــتم\n"
                f"**- الشخـص :** [{replied_user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        args = event.pattern_match.group(2).strip()
        user = None

        if event.reply_to_msg_id:
            replied_message = await event.get_reply_message()
            user = await event.client.get_entity(replied_message.from_id)
        elif args:
            try:
                user = await event.client.get_entity(args)
            except Exception as e:
                return await event.edit(f"**- خطــأ : **`{e}`")

        if not user:
            return await event.edit("**- يرجى تقديم المعرف أو اسم المستخدم، أو الرد على رسالة المستخدم**")

        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
                if str(user.id) in muted_ids:
                    remove_from_mute_list(user.id)
            else:
                result = await event.client.get_permissions(event.chat_id, user.id)
                if result.participant.banned_rights.send_messages:
                    await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        except AttributeError:
            return await edit_or_reply(event, "**- الشخـص غيـر مكـتـوم**")
        except Exception as e:
            return await edit_or_reply(event, f"**- خطــأ : **`{e}`")
        await event.client.send_file(
            event.chat_id,
            joker_unmute,
            caption=f"**- المستخـدم :** {_format.mentionuser(user.first_name, user.id)} \n**- تـم الغـاء كتمـه بنجـاح ✓**",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغــاء_الكــتم\n"
                f"**- الشخـص :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**- الدردشــه :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )

@l313l.ar_cmd(pattern=r"قائمة المكتومين")
async def show_muted_users(event):
    if muted_ids:
        joker_list = "**᯽︙ قائمة المستخدمين المكتومين:**\n"
        tasks = [event.client.get_entity(int(user_id)) for user_id in muted_ids]
        users = await asyncio.gather(*tasks, return_exceptions=True)
        for i, user in enumerate(users, start=1):
            if isinstance(user, Exception):
                joker_list += f"{i}. User ID: {muted_ids[i-1]} (Error: {user})\n"
            else:
                joker_link = f"[{user.first_name}](tg://user?id={user.id})"
                joker_list += f"{i}. {joker_link}\n"
        await event.edit(joker_list)
    else:
        await event.edit("**᯽︙ لا يوجد مستخدمين مكتومين حاليًا**")

# ===================================== # 

@l313l.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "كتم_مؤقت"):
        await event.delete()

#=====================================  #
