from os import environ

from dotenv import load_dotenv

from bot.logging import LOGGER

load_dotenv("config.env", override=True)

API_ID = int(environ.get("API_ID", 0))
API_HASH = environ.get("API_HASH", "")
if API_ID is None or len(API_HASH) == 0:
    LOGGER(__name__).error("Telegram API is missing!")
    exit(1)

BOT_TOKEN = environ.get("BOT_TOKEN", "")
if len(BOT_TOKEN) == 0:
    LOGGER(__name__).error("BOT_TOKEN is missing!")
    exit(1)

BOT_USERNAME = environ.get("BOT_USERNAME", "")
if len(BOT_USERNAME) == 0:
    LOGGER(__name__).error("BOT_USERNAME not provided!")
    exit(1)
if "@" in BOT_USERNAME:
    BOT_USERNAME = BOT_USERNAME.replace("@", "")

list = []
cmd_prfx = environ.get("COMMAND_PREFIXES", "! / .")
if len(cmd_prfx) != 0:
    for cmds in cmd_prfx.split():
        list.append(cmds.strip())
    COMMAND_PREFIXES = dict(prefixes=list)
else:
    COMMAND_PREFIXES = set()

owner = environ.get("OWNER_ID", "")
if len(owner) != 0:
    OWNER_ID = {int(user.strip()) for user in owner.split()}
else:
    LOGGER(__name__).error("OWNER_ID env variable is missing!")
    exit(1)

users = environ.get("SUDO_USERS", "")
if len(users) != 0:
    SUDO_USERS = {int(user.strip()) for user in users.split()}
else:
    SUDO_USERS = set()

UPTOBOX_TOKEN = environ.get("UPTOBOX_TOKEN", "")
if len(UPTOBOX_TOKEN) == 0:
    LOGGER(__name__).warning("UPTOBOX_TOKEN not provided!")
    UPTOBOX_TOKEN = ""

BIFM_URL = environ.get("BIFM_URL", "https://bifm.tacohitbox.com/api/bypass?url")
if len(BIFM_URL) == 0:
    LOGGER(__name__).warning("BIFM_URL not provided! (Using Default)")
    BIFM_URL = "https://bifm.tacohitbox.com/api/bypass?url"

EMILY_API_URL = environ.get("EMILY_API_URL", "")
if len(EMILY_API_URL) == 0:
    LOGGER(__name__).warning("EMILY_API_URL not provided! (Using Default)")
    EMILY_API_URL = "https://api.emilyx.in/api https://emilyapi.fly.dev/api https://emily-api.fly.dev/api"

GDTOT_CRYPT = environ.get("GDTOT_CRYPT", "")
if len(GDTOT_CRYPT) == 0:
    LOGGER(__name__).warning("GDTOT_CRYPT not provided!")
    GDTOT_CRYPT = ""

HUBDRIVE_CRYPT = environ.get("HUBDRIVE_CRYPT", "")
if len(HUBDRIVE_CRYPT) == 0:
    LOGGER(__name__).warning("HUBDRIVE_CRYPT not provided!")
    HUBDRIVE_CRYPT = ""

KATDRIVE_CRYPT = environ.get("KATDRIVE_CRYPT", "")
if len(KATDRIVE_CRYPT) == 0:
    LOGGER(__name__).warning("KATDRIVE_CRYPT not provided!")
    KATDRIVE_CRYPT = ""

KOLOP_CRYPT = environ.get("KOLOP_CRYPT", "")
if len(KOLOP_CRYPT) == 0:
    LOGGER(__name__).warning("KOLOP_CRYPT not provided!")
    KOLOP_CRYPT = ""

DRIVEFIRE_CRYPT = environ.get("DRIVEFIRE_CRYPT", "")
if len(DRIVEFIRE_CRYPT) == 0:
    LOGGER(__name__).warning("DRIVEFIRE_CRYPT not provided!")
    DRIVEFIRE_CRYPT = ""

DRIVEBUZZ_CRYPT = environ.get("DRIVEBUZZ_CRYPT", "")
if len(UPTOBOX_TOKEN) == 0:
    LOGGER(__name__).warning("DRIVEBUZZ_CRYPT not provided!")
    DRIVEBUZZ_CRYPT = ""

DRIVEHUB_CRYPT = environ.get("DRIVEHUB_CRYPT", "")
if len(DRIVEHUB_CRYPT) == 0:
    LOGGER(__name__).warning("DRIVEHUB_CRYPT not provided!")
    DRIVEHUB_CRYPT = ""

GADRIVE_CRYPT = environ.get("GADRIVE_CRYPT", "")
if len(GADRIVE_CRYPT) == 0:
    LOGGER(__name__).warning("GADRIVE_CRYPT not provided!")
    GADRIVE_CRYPT = ""

JIODRIVE_CRYPT = environ.get("JIODRIVE_CRYPT", "")
if len(JIODRIVE_CRYPT) == 0:
    LOGGER(__name__).warning("JIODRIVE_CRYPT not provided!")
    JIODRIVE_CRYPT = ""

Sharerpw_XSRF = environ.get("Sharerpw_XSRF", "")
Sharerpw_laravel = environ.get("Sharerpw_laravel", "")
if len(Sharerpw_XSRF) == 0 or len(Sharerpw_laravel) == 0:
    LOGGER(__name__).warning("Sharer Cookies not provided!")
    Sharerpw_XSRF = ""
    Sharerpw_laravel = ""

UNIFIED_EMAIL = environ.get("UNIFIED_EMAIL", "")
UNIFIED_PASS = environ.get("UNIFIED_PASS", "")
if len(UNIFIED_EMAIL) == 0 or len(UNIFIED_PASS) == 0:
    LOGGER(__name__).warning("Unified Email/Pass not provided!")
    UNIFIED_EMAIL = ""
    UNIFIED_PASS = ""

UPSTREAM_REPO = environ.get("UPSTREAM_REPO", "")
if len(UPSTREAM_REPO) == 0:
    LOGGER(__name__).warning("UPSTREAM_REPO not provided!")
    UPSTREAM_REPO = ""
