from datetime import datetime

import requests as r
from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import *
from bot.helpers.decorators import user_commands

prefixes = COMMAND_PREFIXES
commands = ["ping", f"ping@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def ping(_, message: Message):
    """
    Checks ping speed to bot API
    """

    start = datetime.now()
    r.get("http://api.telegram.org")
    end = datetime.now()

    pong = (end - start).microseconds / 1000
    await message.reply_text(f"**PONG!!** | Ping Time: `{pong}`ms", quote=True)
