import os
from datetime import datetime
import textwrap
from telethon.utils import get_display_name

from JoKeRUB import l313l
from JoKeRUB.core.logger import logging

from ..Config import Config
from ..core import CMD_INFO, PLG_INFO
from ..core.data import _sudousers_list, sudo_enabled_cmds
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import get_user_from_event, mentionuser
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "tools"

LOGS = logging.getLogger(__name__)
ENV = bool(os.environ.get("ENV", False))
JOKDEV = gvarstatus("sudoenable") or "true"


async def _init() -> None:
    sudousers = _sudousers_list()
    Config.SUDO_USERS.clear()
    for user_d in sudousers:
        Config.SUDO_USERS.add(user_d)


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


@l313l.ar_cmd(
    pattern="sudo (تشغيل|ايقاف)$",
    command=("sudo", plugin_category),
    info={
        "header": "لتمكين أو تعطيل صلاحيات السودو في بوتك.",
        "description": "في البداية جميع أوامر السودو معطلة، تحتاج إلى تمكينها باستخدام الأمر addscmd\n تحقق من `{tr}help -c addscmd`",
        "usage": "{tr}sudo <تشغيل/ايقاف>",
    },
)
async def chat_blacklist(event):
    "لتمكين أو تعطيل صلاحيات السودو في بوتك."
    input_str = event.pattern_match.group(1)
    sudousers = _sudousers_list()
    if input_str == "تشغيل":
        if gvarstatus("sudoenable") is not None:
            return await edit_delete(event, "__السودو مفعل بالفعل.__")
        addgvar("sudoenable", "true")
        text = "__تم تفعيل السودو بنجاح.__\n"
        if len(sudousers) != 0:
            text += (
                "**يتم إعادة تحميل البوت لتطبيق التغييرات. يرجى الانتظار لمدة دقيقة**"
            )
            msg = await edit_or_reply(
                event,
                text,
            )
            return await event.client.reload(msg)
        text += "**لم تقم بإضافة أي شخص إلى قائمة السودو بعد.**"
        return await edit_or_reply(
            event,
            text,
        )
    if gvarstatus("sudoenable") is not None:
        delgvar("sudoenable")
        text = "__تم تعطيل السودو بنجاح.__"
        if len(sudousers) != 0:
            text += (
                "**يتم إعادة تحميل البوت لتطبيق التغييرات. يرجى الانتظار لمدة دقيقة**"
            )
            msg = await edit_or_reply(
                event,
                text,
            )
            return await event.client.reload(msg)
        text += "**لم تقم بإضافة أي شخص إلى قائمة السودو بعد.**"
        return await edit_or_reply(
            event,
            text,
        )
    await edit_delete(event, "تم تعطيله بالفعل")


@l313l.ar_cmd(
    pattern="اضف سودو(?:\s|$)([\s\S]*)",
    command=("اضف سودو", plugin_category),
    info={
        "header": "لإضافة مستخدم إلى قائمة السودو.",
        "usage": "{tr}اضف سودو <اسم المستخدم/رد/ذكر>",
    },
)
async def add_sudo_user(event):
    "لإضافة مستخدم إلى قائمة السودو."
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    if replied_user.id == event.client.uid:
        return await edit_delete(event, "__لا يمكنك إضافة نفسك إلى قائمة السودو.__")
    if replied_user.id in _sudousers_list():
        return await edit_delete(
            event,
            f"{mentionuser(get_display_name(replied_user),replied_user.id)} __موجود بالفعل في قائمة السودو.__",
        )
    date = str(datetime.now().strftime("%B %d, %Y"))
    userdata = {
        "chat_id": replied_user.id,
        "chat_name": get_display_name(replied_user),
        "chat_username": replied_user.username,
        "date": date,
    }
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    sudousers[str(replied_user.id)] = userdata
    sql.del_collection("sudousers_list")
    sql.add_collection("sudousers_list", sudousers, {})
    output = f"{mentionuser(userdata['chat_name'],userdata['chat_id'])} __تمت إضافته إلى قائمة السودو.__\n"
    output += "**يتم إعادة تحميل البوت لتطبيق التغييرات. يرجى الانتظار لمدة دقيقة**"
    msg = await edit_or_reply(event, output)
    await event.client.reload(msg)


@l313l.ar_cmd(
    pattern="حذف سودو(?:\s|$)([\s\S]*)",
    command=("حذف سودو", plugin_category),
    info={
        "header": "لحذف مستخدم من قائمة السودو.",
        "usage": "{tr}حذف سودو <اسم المستخدم/رد/ذكر>",
    },
)
async def _(event):
    "لحذف مستخدم من قائمة السودو."
    message_chunks = textwrap.wrap(str(PLG_INFO), width=4000)
    for chunk in message_chunks:
        await event.reply(chunk)
    replied_user, error_i_a = await get_user_from_event(event)
    
    if replied_user is None:
        return
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    if str(replied_user.id) not in sudousers:
        return await edit_delete(
            event,
            f"{mentionuser(get_display_name(replied_user),replied_user.id)} __ليس في قائمة السودو.__",
        )
    del sudousers[str(replied_user.id)]
    sql.del_collection("sudousers_list")
    sql.add_collection("sudousers_list", sudousers, {})
    output = f"{mentionuser(get_display_name(replied_user),replied_user.id)} __تم حذفه من قائمة السودو.__\n"
    output += "**يتم إعادة تحميل البوت لتطبيق التغييرات. يرجى الانتظار لمدة دقيقة**"
    msg = await edit_or_reply(event, output)
    await event.client.reload(msg)


@l313l.ar_cmd(
    pattern="عرض السودو$",
    command=("عرض السودو", plugin_category),
    info={
        "header": "لعرض قائمة مستخدمي السودو.",
        "usage": "{tr}عرض السودو",
    },
)
async def _(event):
    "لعرض قائمة مستخدمي السودو."
    sudochats = _sudousers_list()
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    if len(sudochats) == 0:
        return await edit_delete(
            event, "__لا يوجد مستخدمين في قائمة السودو.__"
        )
    result = "**قائمة مستخدمي السودو:**\n\n"
    for chat in sudochats:
        result += f"☞ **الاسم:** {mentionuser(sudousers[str(chat)]['chat_name'],sudousers[str(chat)]['chat_id'])}\n"
        result += f"**الايدي:** `{chat}`\n"
        username = f"@{sudousers[str(chat)]['chat_username']}" or "__None__"
        result += f"**اسم المستخدم:** {username}\n"
        result += f"تمت الإضافة في {sudousers[str(chat)]['date']}\n\n"
    await edit_or_reply(event, result)


@l313l.ar_cmd(
    pattern="تفعيل سودو(?:s)?(?:\s|$)([\s\S]*)",
    command=("تفعيل سودو", plugin_category),
    info={
        "header": "لتمكين أوامر معينة لمستخدمي السودو.",
        "flags": {
            "-all": "سيقوم بتمكين جميع الأوامر الآمنة لمستخدمي السودو. (باستثناء بعض الأوامر مثل eval, exec, profile).",
            "-full": "سيقوم بتمكين جميع الأوامر بما في ذلك eval, exec...إلخ. (صلاحيات كاملة).",
            "-p": "سيقوم بتمكين جميع الأوامر من الأسماء المحددة للإضافات.",
        },
        "usage": [
            "{tr}تفعيل سودو -all",
            "{tr}تفعيل سودو -full",
            "{tr}تفعيل سودو -p <أسماء الإضافات>",
            "{tr}تفعيل سودو <الأوامر>",
        ],
        "examples": [
            "{tr}تفعيل سودو -p autoprofile botcontrols أي, لأسماء متعددة استخدم مسافة بين كل اسم",
            "{tr}تفعيل سودو ping alive أي, لأوامر متعددة استخدم مسافة بين كل أمر",
        ],
    },
)
async def _(event):  # sourcery no-metrics  # sourcery skip: low-code-quality
    "لتمكين أوامر معينة لمستخدمي السودو."
    input_str = event.pattern_match.group(2)
    errors = ""
    sudocmds = sudo_enabled_cmds()
    if not input_str:
        return await edit_or_reply(
            event, "__ما هي الأوامر التي تريد تمكينها لمستخدمي السودو؟__"
        )
    input_str = input_str.split()
    if input_str[0] == "-all":
        catevent = await edit_or_reply(event, "__جاري تمكين جميع الأوامر الآمنة للسودو....__")
        totalcmds = CMD_INFO.keys()
        flagcmds = (
            PLG_INFO["اوامر الكروب"]
            + PLG_INFO["الوقتي"]
            + PLG_INFO["تحديث"]
            + PLG_INFO["تفرعات الاوامر"]
            + PLG_INFO["معلومات الحساب"]
            + PLG_INFO["اغنية"]
            + PLG_INFO["الادمن"]
            + PLG_INFO["الاوامر"]
            + PLG_INFO["الانتحال"]
            + PLG_INFO["التحكم"]
            + PLG_INFO["التكرار"]
            + ["gauth"]
            + ["greset"]
        )
        loadcmds = list(set(totalcmds) - set(flagcmds))
        if len(sudocmds) > 0:
            sqllist.del_keyword_list("sudo_enabled_cmds")
    elif input_str[0] == "-full":
        catevent = await edit_or_reply(
            event, "__جاري تمكين جميع الأوامر لمستخدمي السودو....__"
        )
        loadcmds = CMD_INFO.keys()
        if len(sudocmds) > 0:
            sqllist.del_keyword_list("sudo_enabled_cmds")
    elif input_str[0] == "-p":
        catevent = event
        input_str.remove("-p")
        loadcmds = []
        for plugin in input_str:
            if plugin not in PLG_INFO:
                errors += (
                    f"`{plugin}` __لا توجد إضافة بهذا الاسم في بوتك.__\n"
                )
            else:
                loadcmds += PLG_INFO[plugin]
    else:
        catevent = event
        loadcmds = []
        for cmd in input_str:
            if cmd not in CMD_INFO:
                errors += f"`{cmd}` __لا يوجد أمر بهذا الاسم في بوتك.__\n"
            elif cmd in sudocmds:
                errors += f"`{cmd}` __تم تمكينه بالفعل لمستخدمي السودو.__\n"
            else:
                loadcmds.append(cmd)
    for cmd in loadcmds:
        sqllist.add_to_list("sudo_enabled_cmds", cmd)
    result = f"__تم تمكين __ `{len(loadcmds)}` __ من الأوامر لمستخدمي السودو.__\n"
    output = (
        result + "**يتم إعادة تحميل البوت لتطبيق التغييرات. يرجى الانتظار لمدة دقيقة**\n"
    )
    if errors != "":
        output += "\n**الأخطاء:**\n" + errors
    msg = await edit_or_reply(catevent, output)
    await event.client.reload(msg)


@l313l.ar_cmd(
    pattern="تعطيل سودو(?:s)?(?:\s|$)([\s\S]*)?",
    command=("تعطيل سودو", plugin_category),
    info={
        "header": "لتعطيل أوامر معينة لمستخدمي السودو.",
        "flags": {
            "-all": "سيقوم بتعطيل جميع الأوامر الممكّنة لمستخدمي السودو.",
            "-flag": "سيقوم بتعطيل جميع الأوامر المميزة مثل eval, exec...إلخ.",
            "-p": "سيقوم بتعطيل جميع الأوامر من الأسماء المحددة للإضافات.",
        },
        "usage": [
            "{tr}تعطيل سودو -all",
            "{tr}تعطيل سودو -flag",
            "{tr}تعطيل سودو -p <أسماء الإضافات>",
            "{tr}تعطيل سودو <الأوامر>",
        ],
        "examples": [
            "{tr}تعطيل سودو -p autoprofile botcontrols أي, لأسماء متعددة استخدم مسافة بين كل اسم",
            "{tr}تعطيل سودو ping alive أي, لأوامر متعددة استخدم مسافة بين كل أمر",
        ],
    },
)
async def _(event):  # sourcery no-metrics  # sourcery skip: low-code-quality
    "لتعطيل أوامر معينة لمستخدمي السودو."
    input_str = event.pattern_match.group(2)
    errors = ""
    sudocmds = sudo_enabled_cmds()
    if not input_str:
        return await edit_or_reply(
            event, "__ما هي الأوامر التي تريد تعطيلها لمستخدمي السودو؟__"
        )
    input_str = input_str.split()
    if input_str[0] == "-all":
        catevent = await edit_or_reply(
            event, "__جاري تعطيل جميع الأوامر الممكّنة للسودو....__"
        )
        flagcmds = sudocmds
    elif input_str[0] == "-flag":
        catevent = await edit_or_reply(
            event, "__جاري تعطيل جميع الأوامر المميزة للسودو.....__"
        )
        flagcmds = (
            PLG_INFO["اوامر الكروب"]
            + PLG_INFO["الوقتي"]
            + PLG_INFO["تحديث"]
            + PLG_INFO["تفرعات الاوامر"]
            + PLG_INFO["معلومات الحساب"]
            + PLG_INFO["اغنية"]
            + PLG_INFO["الادمن"]
            + PLG_INFO["الاوامر"]
            + PLG_INFO["الانتحال"]
            + PLG_INFO["التحكم"]
            + PLG_INFO["التكرار"]
            + ["gauth"]
            + ["greset"]
        )
    elif input_str[0] == "-p":
        catevent = event
        input_str.remove("-p")
        flagcmds = []
        for plugin in input_str:
            if plugin not in PLG_INFO:
                errors += (
                    f"`{plugin}` __لا توجد إضافة بهذا الاسم في بوتك.__\n"
                )
            else:
                flagcmds += PLG_INFO[plugin]
    else:
        catevent = event
        flagcmds = []
        for cmd in input_str:
            if cmd not in CMD_INFO:
                errors += f"`{cmd}` __لا يوجد أمر بهذا الاسم في بوتك.__\n"
            elif cmd not in sudocmds:
                errors += f"`{cmd}` __تم تعطيله بالفعل لمستخدمي السودو.__\n"
            else:
                flagcmds.append(cmd)
    count = 0
    for cmd in flagcmds:
        if sqllist.is_in_list("sudo_enabled_cmds", cmd):
            count += 1
            sqllist.rm_from_list("sudo_enabled_cmds", cmd)
    result = f"__تم تعطيل __ `{count}` __ من الأوامر لمستخدمي السودو.__\n"
    output = (
        result + "**يتم إعادة تحميل البوت لتطبيق التغييرات. يرجى الانتظار لمدة دقيقة**\n"
    )
    if errors != "":
        output += "\n**الأخطاء:**\n" + errors
    msg = await edit_or_reply(catevent, output)
    await event.client.reload(msg)


@l313l.ar_cmd(
    pattern="عرض الأوامر( -d)?$",
    command=("عرض الأوامر", plugin_category),
    info={
        "header": "لعرض قائمة الأوامر الممكّنة أو المعطلة لمستخدمي السودو.",
        "description": "سيظهر لك قائمة بجميع الأوامر الممكّنة أو المعطلة.",
        "flags": {"-d": "لعرض الأوامر المعطلة بدلاً من الممكّنة."},
        "usage": [
            "{tr}عرض الأوامر",
            "{tr}عرض الأوامر -d",
        ],
    },
)
async def _(event):  # sourcery no-metrics
    "لعرض قائمة الأوامر الممكّنة أو المعطلة لمستخدمي السودو."
    input_str = event.pattern_match.group(1)
    sudocmds = sudo_enabled_cmds()
    clist = {}
    error = ""
    if not input_str:
        text = "**قائمة الأوامر الممكّنة لمستخدمي السودو:**"
        result = "**الأوامر الممكّنة**"
        if len(sudocmds) > 0:
            for cmd in sudocmds:
                plugin = get_key(cmd)
                if plugin in clist:
                    clist[plugin].append(cmd)
                else:
                    clist[plugin] = [cmd]
        else:
            error += "__لم تقم بتمكين أي أمر لمستخدمي السودو.__"
        count = len(sudocmds)
    else:
        text = "**قائمة الأوامر المعطلة لمستخدمي السودو:**"
        result = "**الأوامر المعطلة**"
        totalcmds = CMD_INFO.keys()
        cmdlist = list(set(totalcmds) - set(sudocmds))
        if cmdlist:
            for cmd in cmdlist:
                plugin = get_key(cmd)
                if plugin in clist:
                    clist[plugin].append(cmd)
                else:
                    clist[plugin] = [cmd]
        else:
            error += "__لقد قمت بتمكين جميع الأوامر لمستخدمي السودو.__"
        count = len(cmdlist)
    if error != "":
        return await edit_delete(event, error, 10)
    pkeys = clist.keys()
    n_pkeys = [i for i in pkeys if i is not None]
    pkeys = sorted(n_pkeys)
    output = ""
    for plugin in pkeys:
        output += f"• {plugin}\n"
        for cmd in clist[plugin]:
            output += f"`{cmd}` "
        output += "\n\n"
    finalstr = (
        result
        + f"\n\n**SUDO TRIGGER: **`{Config.SUDO_COMMAND_HAND_LER}`\n**الأوامر:** {count}\n\n"
        + output
    )
    await edit_or_reply(event, finalstr, aslink=True, linktext=text)


@l313l.ar_cmd(
    pattern="المساعد$",
    command=("المساعد", plugin_category),
    info={
        "header": "لعرض جميع الأوامر المتاحة.",
        "usage": "{tr}المساعد",
    },
)
async def show_all_commands(event):
    "لعرض جميع الأوامر المتاحة."
    result = "**قائمة جميع الأوامر المتاحة:**\n\n"
    for plugin, cmds in PLG_INFO.items():
        result += f"• **{plugin}**\n"
        for cmd in cmds:
            result += f"`{cmd}` "
        result += "\n\n"
    await edit_or_reply(event, result)


l313l.loop.create_task(_init())
