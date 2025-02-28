import os
import random
import asyncio
import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.channels import CreateChannelRequest, UpdateUsernameRequest
from telethon.tl.functions.account import UpdateUsernameRequest as UpdateAccountUsername
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetPeerDialogsRequest
from .Config import Config
from .core.session import l313l

# إنشاء العميل
bot = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
client = TelegramClient('client_session', api_id, api_hash)

admin = '@GGGCG'
sed = ["off"]

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("**Welcome.\nThis BoT Checker TeLeGram 🐊\n||ProGmMer : [hussien](https://t.me/hussien_pyrogram) .||**", 
                        file="https://telegra.ph/file/70b26b23a9febd3e34f3d.mp4",
                        buttons=[[
                            "– Turbo", f"@{event.sender.username}"
                        ]])

@bot.on(events.NewMessage(pattern='/ Turbo|–'))
async def turbo(event):
    await event.respond("اهلا بك في لوحه تحكم اختيار الرقم \n قم بتحديد الرقم لتذهب الى ازرار تحكم التيربو", 
                        buttons=[
                            ["– Number ①", "– Number ②"],
                            ["– Number ③", "– Number ④"],
                            ["– Number ⑤", "– Number ⑥"],
                            ["– Number ⑦", "– Number ⑧"],
                            ["– Number ⑨", "– Number ①⓪"],
                            ["– Number ①①", "– Number ①②"],
                            ["– Number ①③", "– Number ①④"]
                        ])

@bot.on(events.NewMessage(pattern='/ Number ①|–'))
async def number_one(event):
    await event.respond("Wel .", 
                        buttons=[
                            ["– DeLeTe The Number ①"],
                            ["– Add LiSt ①", "– DeLeTe LiSt ①"],
                            ["– Clicks LiSt ①"],
                            ["– UserName Availble ①"],
                            ["– UserName Last SeeN ①"],
                            ["– Add User in List ①", "– Delete ①"],
                            ["– Edit NaMe ①", "– Edit Bio ①"]
                        ])

@bot.on(events.NewMessage(pattern='/ Clicks LiSt ①|–'))
async def clicks_list(event):
    tr1 = 0
    while True:
        await asyncio.sleep(0.0)
        tr1 += 1
        if "run" in sed:
            await event.respond(f"List NuMber ① : ( {tr1} ) ")
        elif "off" in sed:
            await event.respond("The NuMber ① . OFF 😤")

@bot.on(events.NewMessage(pattern='/ DeLeTe The Number ①|–'))
async def delete_number(event):
    await event.respond("𝚃𝙷𝙴 𝙰𝙲𝙲𝙾𝚄𝙽𝚃 𝙸𝚂 𝙱𝙴𝙸𝙽𝙶 𝙻𝙾𝙶𝙶𝙴𝙳 𝙾𝚄𝚃....")
    await event.respond("𝚂𝙸𝙶𝙽𝙴𝙳 𝙾𝚄𝚃 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 🫠🜾🫠")

@bot.on(events.NewMessage(pattern='/ Add LiSt ①|–'))
async def add_list(event):
    await event.respond("𝐭.", 
                        buttons=[
                            ["– CH ①", "– BotF ①"]
                        ])

@bot.on(events.NewMessage(pattern='/ DeLeTe LiSt ①|–'))
async def delete_list(event):
    await event.respond("I am waiting ...")
    filename = "list.txt"
    if os.path.exists(filename):
        os.remove(filename)
    open(filename, 'x').close()
    await event.respond("DoNe DeLeTe ALL LiSt")

@bot.on(events.NewMessage(pattern='/ Edit NaMe ①|–'))
async def edit_name(event):
    await event.respond("Please SeNd Name NoW\nEx: Ahmed Ali")
    response = await event.get_response()
    jmt = response.text
    await client(UpdateAccountUsername(username=jmt))
    await event.respond(f"تم بنجاح تغيير الاسم الى . {jmt}")

@bot.on(events.NewMessage(pattern='/ Edit Bio ①|–'))
async def edit_bio(event):
    await event.respond("Please SeNd ThE Bio \nEx: hello me ali . . .")
    response = await event.get_response()
    pio = response.text
    await client(UpdateAccountUsername(bio=pio))
    await event.respond(f"تم بنجاح تغيير البايو الى \n {pio}")

@bot.on(events.NewMessage(pattern='/ UserName Availble ①|–'))
async def username_available(event):
    await event.respond(f"اهلا بك عزيزي . {event.sender.first_name} .\nاختر النوع الان من الازرار التاليه . ", 
                        buttons=[
                            ["vip139 - ①", "aaaab"],
                            ["a_b_n - ①", "a_1_n - ①"],
                            ["a_6_1 - ①", "ab111 - ①"],
                            ["aaa111 - ①", "aaabbb - ①"]
                        ])

@bot.on(events.NewMessage(pattern='/ _b_n - ①|a'))
async def a_b_n(event):
    now = datetime.datetime.now()
    await event.respond("DonE , a_b_n - ①")
    c = random.choices('qwertyuiopassdfghjklzxcvbnm')
    d = random.choices('qwertyuiopassdfghjklzxcvbnm')
    s = random.choices('qwertyuiopassdfghjklzxcvbnm')
    f = [c[0], "_", s[0], "_", d[0]]
    username = ''.join(f)
    try:
        await client(GetPeerDialogsRequest(peers=[username]))
        if "tgme_username_link" in username:
            await event.respond(f"متاح . @{username}\n وقت البوت هو . {now}")
    except Exception as e:
        print(e)

@bot.on(events.NewMessage(pattern='/ _1_n - ①|a'))
async def a_1_n(event):
    await event.respond("DonE , a_1_n - ①")
    now = datetime.datetime.now()
    cc = random.choices('qwertyuiopassdfghjklzxcvbnm')
    dd = random.choices('1234567890')
    ss = random.choices('qwertyuiopassdfghjklzxcvbnm')
    f = [cc[0], "_", ss[0], "_", dd[0]]
    username1 = ''.join(f)
    try:
        await client(GetPeerDialogsRequest(peers=[username1]))
        if "tgme_username_link" in username1:
            await event.respond(f"متاح . @{username1}\n وقت البوت هو . {now}")
    except Exception as e:
        print(e)

@bot.on(events.NewMessage(pattern='/ _6_1 - ①|a'))
async def a_6_1(event):
    await event.respond("DonE , a_6_1 - ①")
    ccc = random.choices('qwertyuiopassdfghjklzxcvbnm')
    ddd = random.choices('1234567890')
    sss = random.choices('1234567890')
    f = [ccc[0], "_", sss[0], "_", ddd[0]]
    username = ''.join(f)
    try:
        await client(GetPeerDialogsRequest(peers=[username]))
        if "tgme_username_link" in username:
            await event.respond(f"متاح . @{username}\n وقت البوت هو . {now}")
    except Exception as e:
        print(e)

@bot.on(events.NewMessage(pattern='/aaab - ①|a'))
async def aaaab(event):
    await event.respond("DonE , aaaab - ①")
    now = datetime.datetime.now()
    cb = random.choices('qwertyuiopassdfghjklzxcvbnm')
    db = random.choices('1234567890')
    sb = random.choices('qwertyuiopassdfghjklzxcvbnm')
    f = [cb[0], cb[0], cb[0], cb[0], sb[0]]
    username = ''.join(f)
    random.shuffle(f)
    try:
        await client(GetPeerDialogsRequest(peers=[username]))
        if "tgme_username_link" in username:
            await event.respond(f"متاح . @{username}\n وقت البوت هو . {now}")
    except Exception as e:
        print(e)

@bot.on(events.NewMessage(pattern='/b111 - ①|a'))
async def ab111(event):
    await event.respond("DonE , ab111 - ①")
    now = datetime.datetime.now()
    cq = random.choices('qwertyuiopassdfghjklzxcvbnm')
    dq = random.choices('1234567890')
    sq = random.choices('qwertyuiopassdfghjklzxcvbnm')
    f = [cq[0], sq[0], dq[0], dq[0], dq[0]]
    username = ''.join(f)
    random.shuffle(f)
    try:
        await client(GetPeerDialogsRequest(peers=[username]))
        if "tgme_username_link" in username:
            await event.respond(f"متاح . @{username}\n وقت البوت هو . {now}")
    except Exception as e:
        print(e)

@bot.on(events.NewMessage(pattern='/ip139 - ①|v'))
async def vip139(event):
    await event.respond("DonE , vip - ①")
    now = datetime.datetime.now()
    ka = random.choices('qwertyuiopassdfghjklzxcvbnm')
    fh = random.choices('1234567890')
    kk = random.choices(fh)
    f = ["vip", kk[0], kk[0], kk[0]]
    username = ''.join(f)
    try:
        await client(GetPeerDialogsRequest(peers=[username]))
        if "tgme_username_link" in username:
            await event.respond(f"متاح . @{username}\n وقت البوت هو . {now}")
    except Exception as e:
        print(e)

@bot.on(events.NewMessage(pattern='/aa111 - ①|a'))
async def aaa111(event):
    await event.respond("DonE , aaa111 - ①")
    now = datetime.datetime.now()
    ia = random.choices('qwertyuiopassdfghjklzxcvbnm')
    ds = random.choices('1234567890')
    sb = random.choices('qwertyuiopassdfghjklzxcvbnm')
    f = [ia[0], ia[0], ia[0], ds[0], ds[0], ds[0]]
    username = ''.join(f)
    random.shuffle(f)
    try:
        await client(GetPeerDialogsRequest(peers=[username]))
        if "tgme_username_link" in username:
            await event.respond(f"متاح . @{username}\n وقت البوت هو . {now}")
    except Exception as e:
        print(e)
        ch = await client(CreateChannelRequest(title="عياله احنه البو محمد", about="."))
        await client(UpdateUsernameRequest(channel=ch.chats[0].id, username=username))
        await event.respond(f"تم صيد {username}")

@bot.on(events.NewMessage(pattern='/aabbb - ①|a'))
async def aaabbb(event):
    await event.respond("DonE , aaabbb - ①")
    ia = random.choices('qwertyuiopassdfghjklzxcvbnm')
    ds = random.choices('1234567890')
    ik = random.choices('qwertyuiopassdfghjklzxcvbnm')
    f = [ia[0], ia[0], ia[0], ik[0], ik[0], ik[0]]
    username = ''.join(f)
    random.shuffle(f)
    try:
        await client(GetPeerDialogsRequest(peers=[username]))
        if "tgme_username_link" in username:
            await event.respond(f"متاح . @{username}\n وقت البوت هو . {now}")
    except Exception as e:
        print(e)
        ch = await client(CreateChannelRequest(title="عياله احنه البو محمد", about="."))
        await client(UpdateUsernameRequest(channel=ch.chats[0].id, username=username))
        await event.respond(f"تم صيد {username}")

@bot.on(events.NewMessage(pattern='/ Add User in list ①|–'))
async def add_user(event):
    await event.respond("SeNd The UsEr..")
    response = await event.get_response()
    m = response.text
    if "@" in m:
        m = m.replace("@", "")
        if not ex_id(str(m)):
            with open("list.txt", "a") as f:
                f.write(f"{m}\n")
            await event.respond(f"user : @{m}\nhas been Added to List !")
        else:
            await event.respond("The user is already pined !")

@bot.on(events.NewMessage(pattern='/ DeLeTe ①|–'))
async def delete_user(event):
    d = open("list.txt", "r")
    cs = d.read()
    if cs != "\n":
        await event.respond("Send The User \ndont @")
        response = await event.get_response()
        m = response.text
        if "@" in m:
            m = m.replace("@", "")
        with open("list.txt", "r") as f:
            lines = f.readlines()
        with open("list.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != f"{m}":
                    f.write(line)
                    await event.respond(f"user : {m}\nhas been removed from pin !")
                else:
                    await event.respond("there is no users pinned")

@bot.on(events.NewMessage(pattern='/ UserName Last SeeN ①|–'))
async def username_last_seen(event):
    await event.respond("oky now Locate....", 
                        buttons=[
                            ["ادخال وفحص - ①", "تخمين عشوائي - ①"]
                        ])

@bot.on(events.NewMessage(pattern='/خمين عشوائي - ①|ت'))
async def random_guess(event):
    await event.respond("حدد النوع...", 
                        buttons=[
                            ["vip028 - ①.", "aaaae - ①."],
                            ["ak111 - ①."]
                        ])

@bot.on(events.NewMessage(pattern='/ip028 - ①.|v'))
async def vip028(event):
    bbk = "1234567890"
    km = "vip"
    bh = random.choices(bbk)
    bhton = [km[0], bh[0], bh[0], bh[0]]
    userbam = "".join(bhton)
    kmbe = await client.get_entity(userbam)
    if "UserStatus.LONG_AGO" in kmbe.status:
        await event.respond("جار تخمين يوزر جديد يرجى الانتضار لمده 3 ثواني")
        while True:
            await asyncio.sleep(1)
            await event.respond("①")
            await asyncio.sleep(1)
            await event.respond("②")
            await asyncio.sleep(1)
            await event.respond("③")
            await event.respond(f"@{bhton}\n{kmbe.status.was_online}")

@bot.on(events.NewMessage(pattern='/aaae - ①.|a'))
async def aaaae(event):
    turb = random.choices('qwertyuiopassdfghjklzxcvbnm')
    bh = random.choices('qwertyuiopassdfghjklzxcvbnm')
    bhton1 = [turb[0], bh[0], bh[0], bh[0], bh[0]]
    useram = "".join(bhton1)
    kmbe = await client.get_entity(useram)
    if "UserStatus.LONG_AGO" in kmbe.status:
        await event.respond("جار تخمين يوزر جديد يرجى الانتضار لمده 3 ثواني")
        while True:
            await asyncio.sleep(1)
            await event.respond("①")
            await asyncio.sleep(1)
            await event.respond("②")
            await asyncio.sleep(1)
            await event.respond("③")
            await event.respond(f"@{bhton1}\n{kmbe.status.was_online}")

@bot.on(events.NewMessage(pattern='/b111 - ①.|a'))
async def ab111_1(event):
    cq = random.choices('qwertyuiopassdfghjklzxcvbnm')
    dq = random.choices('1234567890')
    sq = random.choices('qwertyuiopassdfghjklzxcvbnm')
    f = [cq[0], sq[0], dq[0], dq[0], dq[0]]
    username4 = ''.join(f)
    random.shuffle(f)
    kmbe = await client.get_entity(username4)
    if "UserStatus.LONG_AGO" in kmbe.status:
        await event.respond("جار تخمين يوزر جديد يرجى الانتضار لمده 3 ثواني")
        while True:
            await asyncio.sleep(1)
            await event.respond("①")
            await asyncio.sleep(1)
            await event.respond("②")
            await asyncio.sleep(1)
            await event.respond("③")
            await event.respond(f"username:. @{username4}\n{kmbe.status.was_online}")

@bot.on(events.NewMessage(pattern='/ دخال وفحص - ①|ا'))
async def check_username(event):
    await event.respond("SENd UserName")
    response = await event.get_response()
    kh = response.text
    kn = await client.get_entity(kh)
    await event.respond(f"User: @{kh}\n{kn.status.was_online}")

@bot.on(events.NewMessage(pattern='/ BotF ①|–'))
async def botf(event):
    await event.respond("send UsErs Now")
    response = await event.get_response()
    Us = response.text
    await event.respond(f"Done Start users")
    sed.clear()
    sed.append("run")
    await client.send_message("botfather", "/newbot")
    for i in range(10000000000000000):
        break
    with open("list.txt", "r+") as f:
        f.write(f"{Us}\n")
    try:
        k = open("list.txt", "a")
        user = k.write(f"{Us}")
        await client(GetPeerDialogsRequest(peers=[user]))
    except Exception as e:
        print(e)
    if "tgme_username_link" in Us:
        try:
            await client.send_message("BotFather", f"{Us}")
            await event.respond(f"تم الصيد .! @{Us}")
        except:
            await event.respond(f"حدث خطا مع {user}")

@bot.on(events.NewMessage(pattern='/ CH ①|–'))
async def ch(event):
    await event.respond("**||Send UsErS in LiSt**||\nEx: bbbfb\njjjij\nkkkk1\nvip89**||")
    response = await event.get_response()
    ui = response.text
    sed.clear()
    sed.append("run")
    with open("list.txt", "r+") as f:
        f.write(f"{ui}\n")
    try:
        k = open("list.txt", "a")
        user = k.write(f"{ui}")
        await client(GetPeerDialogsRequest(peers=[user]))
    except Exception as e:
        print(e)
    if "tgme_username_link" in ui:
        try:
            ch = await client(CreateChannelRequest(title="A.b 🇮🇶", about="."))
            await client(UpdateUsernameRequest(channel=ch.chats[0].id, username=ui))
            msu = await client.get_me()
            await event.respond(f"نحن الاقوى . 🐊\n المعرف : @{ui}\nالرقم : {msu.phone}")
        except:
            await event.respond(f"حدث خطا مع {ui}")
        with open("list.txt", "a") as f:
            f.write(f"\n@{ui}")
            sed.clear()
            sed.append("run")
            return

def ex_id(username):
    with open("list.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if username in line:
                return True
        return False

with bot:
    bot.run_until_disconnected()
print("شغال")
