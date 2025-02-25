@l313l.ar_cmd(
    pattern="(ت(ل)?ك(راف)?) ?(m|t|ميديا|نص)(?:\s|$)([\s\S]*)",
    command=("تلكراف", plugin_category),
    info={
        "header": "To get telegraph link.",
        "description": "Reply to text message to paste that text on telegraph you can also pass input along with command \
            So that to customize title of that telegraph and reply to media file to get sharable link of that media(atmost 5mb is supported)",
        "options": {
            "m or media": "To get telegraph link of replied sticker/image/video/gif.",
            "t or text": "To get telegraph link of replied text you can use custom title.",
        },
        "usage": [
            "{tr}tgm",
            "{tr}tgt <title(optional)>",
            "{tr}telegraph media",
            "{tr}telegraph text <title(optional)>",
        ],
    },
)
async def _(event):
    "To get telegraph link."
    jokevent = await edit_or_reply(event, "` ⌔︙جـار انشـاء رابـط تلكـراف`")
    optional_title = event.pattern_match.group(5)
    if not event.reply_to_msg_id:
        return await jokevent.edit(
            "` ⌔︙قـم بالـرد عـلى هـذه الرسـالة للحـصول عـلى رابـط تلكـراف فـورا`",
        )

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()

    if input_str in ["ميديا", "m"]:
        try:
            # تحميل الملف
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await jokevent.edit(f"` ⌔︙تـم التحـميل الـى {downloaded_file_name}`")

            # إذا كان الملف من نوع .webp، نقوم بتحويله
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)

            # رفع الملف إلى graph.org
            try:
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await jokevent.edit(f"** ⌔︙خـطأ : **\n`{exc}`")
                os.remove(downloaded_file_name)
                return

            # حساب الوقت المستغرق
            end = datetime.now()
            ms = (end - start).seconds

            # تغيير النطاق من telegra.ph إلى graph.org
            media_url = f"https://graph.org{media_urls[0]}"

            # إرسال الرابط
            await jokevent.edit(
                f"** ⌔︙الـرابـط : **[إضـغط هنـا]({media_url})\
                    \n** ⌔︙الوقـت المأخـوذ : **`{ms} ثـانيـة.`",
                link_preview=False,
            )

            # حذف الملف المؤقت
            os.remove(downloaded_file_name)

        except Exception as e:
            await jokevent.edit(f"** ⌔︙حـدث خـطأ : **\n`{str(e)}`")
            if os.path.exists(downloaded_file_name):
                os.remove(downloaded_file_name)

    elif input_str in ["نص", "t"]:
        user_object = await event.client.get_entity(r_message.sender_id)
        title_of_page = get_display_name(user_object)
        # apparently, all Users do not have last_name field
        if optional_title:
            title_of_page = optional_title
        page_content = r_message.message
        if r_message.media:
            if page_content != "":
                title_of_page = page_content
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TEMP_DIR
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            for m in m_list:
                page_content += m.decode("UTF-8") + "\n"
            os.remove(downloaded_file_name)
        page_content = page_content.replace("\n", "<br>")
        try:
            response = telegraph.create_page(title_of_page, html_content=page_content)
        except Exception as e:
            LOGS.info(e)
            title_of_page = "".join(
                random.choice(list(string.ascii_lowercase + string.ascii_uppercase))
                for _ in range(16)
            )
            response = telegraph.create_page(title_of_page, html_content=page_content)
        end = datetime.now()
        ms = (end - start).seconds
        joker = f"https://graph.org/{response['path']}"
        await jokevent.edit(
            f"** ⌔︙الـرابـط : ** [اضغـط هنـا]({joker})\
                 \n** ⌔︙الـوقـت المـأخـوذ : **`{ms} ثـانيـة.`",
            link_preview=False,
            )
