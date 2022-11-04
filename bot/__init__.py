import logging
import os

import telegram.ext as tg
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

load_dotenv("config.env", override=True)


class ENV_VARS(object):
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BIFM_URL = os.environ.get("BIFM_URL", "https://bifm.tacohitbox.com/api/bypass?url")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    BOT_USERNAME = os.environ.get("BOT_USERNAME")
    GDTOT_CRYPT = os.environ.get("GDTOT_CRYPT")
    UNIFIED_EMAIL = os.environ.get("UNIFIED_EMAIL")
    UNIFIED_PASS = os.environ.get("UNIFIED_PASS")
    HUBDRIVE_CRYPT = os.environ.get("HUBDRIVE_CRYPT")
    KATDRIVE_CRYPT = os.environ.get("KATDRIVE_CRYPT")
    KOLOP_CRYPT = os.environ.get("KOLOP_CRYPT")
    DRIVEFIRE_CRYPT = os.environ.get("DRIVEFIRE_CRYPT")
    DRIVEBUZZ_CRYPT = os.environ.get("DRIVEBUZZ_CRYPT")
    GADRIVE_CRYPT = os.environ.get("GADRIVE_CRYPT")
    JIODRIVE_CRYPT = os.environ.get("JIODRIVE_CRYPT")
    Sharerpw_XSRF = os.environ.get("Sharerpw_XSRF")
    Sharerpw_laravel = os.environ.get("Sharerpw_laravel")
    EMILY_API_URL = os.environ.get("EMILY_API_URL", "https://api.emilyx.in/api")
    UPTOBOX_TOKEN = os.environ.get("UPTOBOX_TOKEN")
    AUTH_USER = int(os.environ.get("AUTH_USER", 0))
    MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", 4096))


Config = ENV_VARS
handler = Config.BOT_USERNAME
tg_bot = Config.BOT_TOKEN

updater = tg.Updater(
    token=tg_bot, request_kwargs={"read_timeout": 30, "connect_timeout": 15}
)
bot = updater.bot


class CMD(object):
    START = ["start", f"start@{handler}"]
    HELP = ["help", f"help@{handler}"]
    TEML = ["teml", f"teml@{handler}"]
    RUNF = ["eval", f"eval@{handler}"]
    BIFM = ["bifm", f"bifm@{handler}"]
    DIRT = ["direct", f"direct@{handler}"]
    BYPS = ["bypass", f"bypass@{handler}"]
    AIO = ["multi", f"multi@{handler}"]
    SHRT = ["shorten", f"shorten@{handler}"]
    INDX = ["index", f"index@{handler}"]
    MGNT = ["magnet", f"magnet@{handler}"]
    SCRP = ["scrape", f"scrape@{handler}"]
    GDFS = ["gd", f"gd@{handler}"]
