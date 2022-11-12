import time

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import BotStartTime
from bot.config import *
from bot.helpers.decorators import user_commands
from bot.helpers.functions import get_readable_time
from bot.version import (
    __bot_version__,
    __gitrepo__,
    __license__,
    __pyro_layer__,
    __pyro_version__,
    __python_version__,
)

START_TEXT = """<b>Hey there!!</b>\n<b><i>I am the Multi Function Bot.</i></b>\n<i>Use buttons to navigate and know more about me :) \n\n**Bot is alive since {}.**</i>"""

COMMAND_TEXT = """**Here are the list of commands wich you can use in bot.\n**"""

ABOUT_TEXT = f"""• **Python Version** : {__python_version__}
• **Bot Version** : {__bot_version__}
• **Pyrogram Version** : {__pyro_version__}
• **Pyrogram Layer** : {__pyro_layer__}
• **License** : {__license__}

**Github Repo**: {__gitrepo__}"""

USER_TEXT = """🗒️ Documentation for commands available to user's

• /start: To Get this message

• /help: Alias command for start

• /ping: Ping the telegram api server.

• /bifm - Bypass Short Links using BIFM API

• /direct - Get Direct Link for various Supported URLs

• /bypass - Bypass Various Supported Shortened URLs

• /multi - Bypass Short Links using PyBypass Library

• /shorten - Get AdFree Shortened URLs of your Link

• /magnet - Extract Magnet from Torrent Websites

• /index - Extract Direct Links from Bhadoo Index Folder URLs

• /scrape - Extract Direct Links from Supported Sites

• /gd - Get GDrive Links for various Drive File Sharer
"""

SUDO_TEXT = """
🗒️ Documentation for Sudo Users commands.

• /speedtest: Check the internet speed of bot server.

• /serverstats: Get the stats of server.

• /stats: Alias command for serverstats
"""

DEV_TEXT = """
🗒️ Documentation for Developers Commands.

• /update: To update the bot to latest commit from repository.

• /restart: Restart the bot.

• /log: To get the log file of bot.

• /ip: To get ip of the server where bot is running

• /shell: To run the terminal commands via bot.

• /exec: To run the python commands via bot
"""

START_BUTTON = [
    [
        InlineKeyboardButton("📖 Commands", callback_data="COMMAND_BUTTON"),
        InlineKeyboardButton("👨‍💻 About me", callback_data="ABOUT_BUTTON"),
    ],
    [
        InlineKeyboardButton(
            "🔭 Original Repo",
            url=f"{__gitrepo__}",
        )
    ],
]

COMMAND_BUTTON = [
    [
        InlineKeyboardButton("Users", callback_data="USER_BUTTON"),
        InlineKeyboardButton("Sudo", callback_data="SUDO_BUTTON"),
    ],
    [InlineKeyboardButton("Developer", callback_data="DEV_BUTTON")],
    [InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")],
]

GOBACK_1_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")]]

GOBACK_2_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="COMMAND_BUTTON")]]

prefixes = COMMAND_PREFIXES
commands = ["start", f"start@{BOT_USERNAME}", "help", f"help@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def start(client, message):
    botuptime = get_readable_time(time.time() - BotStartTime)
    await message.reply_text(
        text=START_TEXT.format(botuptime),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(START_BUTTON),
    )


@Client.on_callback_query()
async def botCallbacks(client, CallbackQuery):
    user_id = CallbackQuery.from_user.id

    if CallbackQuery.data == "ABOUT_BUTTON":
        await CallbackQuery.edit_message_text(
            ABOUT_TEXT,
            reply_markup=InlineKeyboardMarkup(GOBACK_1_BUTTON),
            disable_web_page_preview=True,
        )

    elif CallbackQuery.data == "START_BUTTON":
        await CallbackQuery.edit_message_text(
            START_TEXT, reply_markup=InlineKeyboardMarkup(START_BUTTON)
        )

    elif CallbackQuery.data == "COMMAND_BUTTON":
        await CallbackQuery.edit_message_text(
            COMMAND_TEXT, reply_markup=InlineKeyboardMarkup(COMMAND_BUTTON)
        )

    elif CallbackQuery.data == "USER_BUTTON":
        await CallbackQuery.edit_message_text(
            USER_TEXT, reply_markup=InlineKeyboardMarkup(GOBACK_2_BUTTON)
        )

    elif CallbackQuery.data == "SUDO_BUTTON":
        if user_id not in SUDO_USERS:
            return await CallbackQuery.answer(
                "You are not in the sudo user list.", show_alert=True
            )
        else:
            await CallbackQuery.edit_message_text(
                SUDO_TEXT, reply_markup=InlineKeyboardMarkup(GOBACK_2_BUTTON)
            )

    elif CallbackQuery.data == "DEV_BUTTON":
        if user_id not in OWNER_ID:
            return await CallbackQuery.answer(
                "This is developer restricted command.", show_alert=True
            )
        else:
            await CallbackQuery.edit_message_text(
                DEV_TEXT, reply_markup=InlineKeyboardMarkup(GOBACK_2_BUTTON)
            )
