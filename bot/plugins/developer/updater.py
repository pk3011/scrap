import os
import subprocess
import sys
import time

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import *
from bot.helpers.decorators import dev_commands
from bot.logging import LOGGER

prefixes = COMMAND_PREFIXES

commands = ["update", f"update@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@dev_commands
async def update(client, message: Message):
    """
    Update the bot with latest commit changes from GitHub.
    """

    msg = await message.reply_text(
        "**Pulling changes with latest commits...**", quote=True
    )
    if UPSTREAM_REPO is not None:
        if os.path.exists(".git"):
            subprocess.run(["rm", "-rf", ".git"])
        update = subprocess.run(
            [
                f"git init -q \
                            && git config --global user.email emilymiss22@gmail.com \
                            && git config --global user.name multifbot \
                            && git add . \
                            && git commit -sm update -q \
                            && git remote add origin {UPSTREAM_REPO} \
                            && git fetch origin -q \
                            && git reset --hard origin/main -q"
            ],
            shell=True,
        )
        time.sleep(1.5)
        if update.returncode == 0:
            LOGGER(__name__).info(
                "Successfully updated with latest commit from UPSTREAM_REPO"
            )
        else:
            LOGGER(__name__).error(
                "Something went wrong while updating, check UPSTREAM_REPO if valid or not!"
            )
        time.sleep(2)
        LOGGER(__name__).info("Bot Updated with latest commits. Restarting now..")
        await msg.edit(
            "**Changes pulled with latest commits. Restarting bot now... 🌟**"
        )
        os.execl(sys.executable, sys.executable, "-m", "bot")
        sys.exit()
    else:
        await msg.edit(
            "**UpStream Repo not Provided, so could not fetch updates... 🌟**"
        )


commands = ["restart", f"restart@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@dev_commands
async def restart(client, message: Message):
    """
    Restart the bot.
    """

    LOGGER(__name__).info("Restarting the bot. Shutting down this instance")
    print("ok")
    await message.reply_text(
        "`Starting a new instance and shutting down this one`", quote=True
    )
    os.execl(sys.executable, sys.executable, "-m", "bot")
    sys.exit()
