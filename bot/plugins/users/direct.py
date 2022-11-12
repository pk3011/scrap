from re import search
from time import sleep, time

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import *
from bot.helpers.decorators import user_commands
from bot.helpers.functions import get_readable_time
from bot.logging import LOGGER
from bot.modules import direct_link
from bot.modules.lists import *
from bot.modules.pasting import telegraph_paste
from bot.modules.regex import *

prefixes = COMMAND_PREFIXES
commands = ["direct", f"direct@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def direct(_, message: Message):
    """
    Get Direct Link for various Supported URLs
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
    sleep(1)
    is_artstation = is_artstation_link(url)
    if is_artstation:
        link_type = "ArtStation"
        res = direct_link.artstation(url)
    elif "mdisk." in url:
        link_type = "MDisk"
        res = direct_link.mdisk(url)
        res2 = direct_link.mdisk_mpd(url)
    elif "wetransfer." in url or "we.tl" in url:
        link_type = "WeTransfer"
        res = direct_link.wetransfer(url)
    elif "gdbot." in url:
        link_type = "GDBot"
        res = direct_link.gdbot(url)
    elif "gofile." in url:
        link_type = "GoFile"
        # res = direct_link.gofile(url)
        res = url  # Temporary Solution
    elif "megaup." in url:
        link_type = "MegaUp"
        res = direct_link.megaup(url)
    elif "sfile.mobi" in url:
        link_type = "Sfile.mobi"
        res = direct_link.sfile(url)
    elif any(x in url for x in yandisk_list):
        link_type = "Yandex Disk"
        res = direct_link.yandex_disk(url)
    elif "osdn." in url:
        link_type = "OSDN"
        res = direct_link.osdn(url)
    elif "github.com" in url:
        link_type = "Github"
        res = direct_link.github(url)
    elif "mediafire." in url:
        link_type = "MediaFire"
        res = direct_link.mediafire(url)
    elif "zippyshare." in url:
        link_type = "ZippyShare"
        res = direct_link.zippyshare(url)
    elif "hxfile." in url:
        link_type = "HXFile"
        res = direct_link.hxfile(url)
    elif "files.im" in url:
        link_type = "FilesIm"
        res = direct_link.filesIm(url)
    elif "anonfiles." in url:
        link_type = "AnonFiles"
        res = direct_link.anonfiles(url)
    elif "letsupload." in url:
        link_type = "LetsUpload"
        res = direct_link.letsupload(url)
    elif "linkpoi." in url:
        link_type = "LinkPoi"
        res = direct_link.linkpoi(url)
    elif any(x in url for x in fmed_list):
        link_type = "Fembed"
        res = direct_link.fembed(url)
    elif any(x in url for x in sbembed_list):
        link_type = "SBEmbed"
        res = direct_link.sbembed(url)
    elif "mirrored." in url:
        link_type = "Mirrored"
        res = direct_link.mirrored(url)
    elif "reupload." in url:
        link_type = "ReUpload"
        res = direct_link.reupload(url)
    elif "uservideo." in url:
        link_type = "UserVideo"
        res = direct_link.uservideo(url)
    elif "antfiles." in url:
        link_type = "AntFiles"
        res = direct_link.antfiles(url)
    elif "streamtape." in url:
        link_type = "StreamTape"
        res = direct_link.streamtape(url)
    elif "sourceforge" in url:
        link_type = "SourceForge"
        if "master.dl.sourceforge.net" in url:
            res = direct_link.sourceforge2(url)
        else:
            res = direct_link.sourceforge(url)
    elif "androidatahost." in url:
        link_type = "AndroidataHost"
        res = direct_link.androiddatahost(url)
    elif "krakenfiles." in url:
        link_type = "KrakenFiles"
        res = direct_link.krakenfiles(url)
    elif "dropbox." in url:
        link_type = "DropBox"
        if "dropbox.com/s/" in url:
            res = direct_link.dropbox(url)
        else:
            res = direct_link.dropbox2(url)
    elif "pixeldrain." in url:
        link_type = "PixelDrain"
        res = direct_link.pixeldrain(url)
    elif "streamlare." in url:
        link_type = "Streamlare"
        res = direct_link.streamlare(url)
    elif "pandafiles." in url:
        link_type = "PandaFiles"
        res = direct_link.pandafile(url)
    elif "1fichier." in url:
        link_type = "Fichier"
        res = direct_link.fichier(url)
    elif "upload.ee" in url:
        link_type = "UploadEE"
        res = direct_link.uploadee(url)
    elif "uptobox." in url:
        link_type = "Uptobox"
        res = direct_link.uptobox(url)
    elif "solidfiles." in url:
        link_type = "SolidFiles"
        res = direct_link.solidfiles(url)
    elif "hubcloud." in url:
        link_type = "HubCloud"
        res = direct_link.hubcloud(url)
    elif "bunkr.is" in url:
        link_type = "Bunkr.is"
        res = direct_link.bunkr_cyber(url)
        res = telegraph_paste(res)
    elif "cyberdrop." in url:
        link_type = "CyberDrop"
        res = direct_link.bunkr_cyber(url)
        res = telegraph_paste(res)
    elif "pixl.is" in url:
        link_type = "Pixl.is"
        res = direct_link.pixl(url)
        res = telegraph_paste(res)
    elif "send.cm" in url:
        is_sendcm_folder = is_sendcm_folder_link(url)
        if is_sendcm_folder:
            link_type = "Sendcm Folder"
            res = direct_link.sendcm(url)
            res = telegraph_paste(res)
        else:
            link_type = "Sendcm File"
            res = direct_link.sendcm(url)
    elif any(x in url for x in linkvertise_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in bypass_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in adfly_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in scrape_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Site Scraper</b>\n\n<i>Use it with /scrape command followed by Link</i>"
        await msg.edit(text=err)
        return
    else:
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b><i>Could not generate Direct Link for your URL</i></b>"
        await message.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    LOGGER(__name__).info(f" Received : {cmd} - {link_type} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n<b>Link Type</b> : <i>{link_type}</i>"
    await msg.edit(text=abc)
    sleep(1)
    time_taken = get_readable_time(time() - start)
    LOGGER(__name__).info(f" Destination : {cmd} - {res}")
    if link_type == "GoFile":
        xyz = f"<b><i>Sorry! GoFile Bypass is not supported anymore</i></b>"
    elif link_type == "MDisk":
        xyz = f"<b><i>Download Link: {res}\n MPD Link: {res2}</i></b>\n\n<i>Time Taken : {time_taken}</i>"
    elif link_type == "MegaUp":
        xyz = (
            f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b><i>Your Direct-Download Link is :</i></b>\n<code>{res}</code>\n\n"
            f"<b><u>NOTE : </u></b>\n<i>MegaUp has Cloudflare Protection Enabled.So Do not use this Link in Mirror Bots.Use it from your Device and downloading will start.</i>"
        )
    elif (
        link_type == "Bunkr.is"
        or link_type == "CyberDrop"
        or link_type == "Pixl.is"
        or link_type == "Sendcm Folder"
    ):
        xyz = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b><i>Your Telegraph URL (containing Result) is :\n</i></b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    else:
        xyz = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b><i>Your Direct-Download Link is :\n</i></b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    await message.reply_text(text=xyz, disable_web_page_preview=True, quote=True)
