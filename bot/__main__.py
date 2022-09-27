import logging
import os
from bot import Config
from pyrogram import Client, __version__
from pyrogram.raw.all import layer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

plugins = dict(
    root="bot/modules"
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "MultiFunction",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=plugins
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        un = "@" + me.username
        LOGGER.info("Installing Bot Requirements...")
        os.system("pip3 install --no-cache-dir -r requirements.txt --upgrade")
        LOGGER.info(f"Pyrogram v{__version__} (Layer {layer}) started on {un}.")
        LOGGER.info("Telegram Bot Started.")

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("Bot Stopped ! Bye..........")


if __name__ == "__main__":
    app = Bot()
    app.run()