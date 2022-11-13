from re import search
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import *
from bot.helpers.decorators import user_commands
from bot.helpers.functions import get_readable_time
from bot.logging import LOGGER
from bot.modules import scraper
from bot.modules.pasting import telegraph_paste
from bot.modules.regex import URL_REGEX, is_a_url

prefixes = COMMAND_PREFIXES
commands = ["index", f"index@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def index(_, message: Message):
    """
    Extract Direct Links from Bhadoo Index Folder URLs
    """
    msg_arg = message.text.replace("  ", " ")
    msg_args = msg_arg.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(msg_args) > 1:
        cmd = msg_args[0]
        url = msg_args[1]
    elif reply_to is not None:
        try:
            reply_text = search(URL_REGEX, reply_to.text)[0]
        except BaseException:
            reply_text = (
                search(URL_REGEX, str(reply_to.caption))[0]
                .replace("\\", "")
                .split("*")[0]
            )
        url = reply_text.strip()
        cmd = msg_args[0]
    elif msg_args.count == (0 or 1) or reply_to is None:
        return "Bot could not retrieve your Input!"

    if url is not None:
        if url.startswith("http://"):
            url = url.replace("http://", "https://")
        elif not url.startswith("https://"):
            url = "https://" + url
    else:
        return "Bot could not retrieve your URL!"

    valid_url = is_a_url(url)
    if valid_url is not True:
        return "You did not seem to have entered a valid URL!"
    uname = message.from_user.mention
    uid = f"<code>{message.from_user.id}</code>"
    start = time()
    LOGGER(__name__).info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Bhadoo Index</i>"
    await message.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = scraper.index_scrap(url)
    des_url = telegraph_paste(res)
    time_taken = get_readable_time(time() - start)
    LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
    xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    await message.reply_text(text=xyz, disable_web_page_preview=True, quote=True)
