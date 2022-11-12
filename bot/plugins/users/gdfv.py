from re import search
from time import sleep, time

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers.decorators import user_commands
from bot.helpers.functions import get_readable_time
from bot.logging import LOGGER
from bot.modules.gdrive_direct import *
from bot.modules.regex import *

prefixes = COMMAND_PREFIXES
commands = ["gd", f"gd@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def gd(_, message: Message):
    """
    Get GDrive Links for various Drive File Sharer
    """
    msg_args = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(msg_args) > 1:
        cmd = msg_args[0]
        url = msg_args[1]
    elif reply_to is not None:
        try:
            reply_text = search(URL_REGEX, reply_to.text)[0]
        except BaseException:
            reply_text = (
                search(URL_REGEX, reply_to.caption_markdown_v2)[0]
                .replace("\\", "")
                .split("*")[0]
            )
        url = reply_text.strip()
        cmd = msg_args[0]
    else:
        return "Bot could not retrieve your URL!"
    valid_url = is_a_url(url)
    if valid_url is not True or url is None:
        return "You did not seem to have entered a valid URL!"
    uname = message.from_user.mention
    uid = f"<code>{message.from_user.id}</code>"
    start = time()
    msg_text = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Processing your URL.....</b>"
    msg = await message.reply_text(
        text=msg_text, disable_web_page_preview=True, quote=True
    )
    LOGGER(__name__).info(f" Received : {cmd} - {url}")
    sleep(1)
    is_gdtot = is_gdtot_link(url)
    is_drivehubs = is_drivehubs_link(url)
    is_unified = is_unified_link(url)
    is_udrive = is_udrive_link(url)
    is_sharer = is_sharer_link(url)
    if is_gdtot:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>GDTot</i>"
        await msg.edit(text=abc)
        res = gdtot(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif is_drivehubs:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>DriveHubs</i>"
        await msg.edit(text=abc)
        res = drivehubs(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif is_unified:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>AppDrive Look-Alike</i>"
        await msg.edit(text=abc)
        res = unified(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif is_udrive:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>HubDrive Look-Alike</i>"
        await msg.edit(text=abc)
        res = udrive(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif is_sharer:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Sharer.pw</i>"
        await msg.edit(text=abc)
        res = sharerpw(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif "pahe." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Pahe</i>"
        await msg.edit(text=abc)
        res = pahe(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif "drive.google.com" in url:
        xyz = "You have entered a Google Drive Link!"
    else:
        xyz = "This Command does not support this Link!"
    sleep(1)
    await message.reply_text(text=xyz, disable_web_page_preview=True, quote=True)
