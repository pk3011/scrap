import time
from re import search

import cloudscraper
from pyrogram import Client, __version__, filters
from pyrogram.raw.all import layer

from bot import CMD, LOGGER, Config
from bot.helpers.utilities import bypasser, direct_link, shortener
from bot.helpers.utilities.gdrive_direct import (
    drivehubs,
    gdtot,
    pahe,
    sharerpw,
    udrive,
    unified,
)
from bot.helpers.utilities.lists import (
    bypass_list,
    directdl_list,
    fmed_list,
    linkvertise_list,
    sbembed_list,
    scrape_list,
    shst_list,
    yandisk_list,
)
from bot.helpers.utilities.regex import (
    URL_REGEX,
    is_a_url,
    is_artstation_link,
    is_drivehubs_link,
    is_gdtot_link,
    is_sendcm_folder_link,
    is_sharer_link,
    is_udrive_link,
    is_unified_link,
)
from bot.helpers.utilities.scraper import (
    atishmkv_scrap,
    cinevez_scrap,
    cinevood_scrap,
    filecrypt_scrap,
    htpmovies_scrap,
    igggames_scrape,
    index_scrap,
    magnet_scrap,
    moviesdrama_scrap,
    privatemoviez_scrape,
    olamovies_scrap,
    sharespark_scrap,
    toonworld4all_scrap,
)

dom = Config.EMILY_API_URL
api = f"{dom}/paste"


def telegraph_paste(res):
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "telegraph_paste", "text": res})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


@Client.on_message(filters.command(CMD.START))
async def start(bot, update):
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    msg = f"Hello {uname} (ID: {uid}),\n<b><i>I am the Multi Function Bot</i></b>\n\n<i>Use /help to get more Information about the Bot.</i>\n\n"
    msg += f"<b>Pyrogram</b> Version : <i>v{__version__}(Layer {layer})</i>\n\n"
    msg += "<b><i>Made with Love by Miss Emily\n(https://github.com/missemily2022)</i></b>\n\n"
    msg += "<b>Important:<i> Bot does not support Reply to Link Support. Only command followed by link is supported.</i></b>"
    await update.reply_text(
        text=msg,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(filters.command(CMD.HELP))
async def help(bot, update):
    tuv = "<b>Bot supports the following commands</b>‌ :-</b>\n"
    tuv += "\n• <i>Use /bifm to Bypass Short Links using BIFM API</i>"
    tuv += "\n• <i>Use /direct to get Direct Link for various Supported URLs</i>"
    tuv += "\n• <i>Use /bypass to Bypass Various Supported Shortened URLs</i>"
    tuv += "\n• <i>Use /droplink to Bypass Droplink URLs</i>"
    tuv += "\n• <i>Use /gplink to Bypass GpLinks URLs</i>"
    tuv += "\n• <i>Use /linkvertise to Bypass Linkvertise URLs</i>"
    tuv += "\n• <i>Use /adfly to Bypass AdFly URLs</i>"
    tuv += "\n• <i>Use /sirigan to Bypass sirigan.my.id URLs</i>"
    tuv += "\n• <i>Use /ouo to Bypass ouo.io and ouo.press URLs</i>"
    tuv += "\n• <i>Use /shorte to Bypass shorte URLs</i>"
    tuv += "\n• <i>Use /multi to Bypass Short Links using bypass.vip API</i>"
    tuv += "\n• <i>Use /rocklink for URLs to Bypass RockLinks URLs</i>"
    tuv += "\n• <i>Use /magnet to Extract Magnets from Torrent Websites</i>"
    tuv += "\n• <i>Use /shorten to get Shortened Version of your URLs</i>"
    tuv += "\n• <i>Use /index to extract Direct Links from Bhadoo Index Folder URLs (which do not have any kind of Protection)</i>"
    # tuv += "\n• <i>Use /psa to Extract Download Links from psa.pm URLs</i>"
    tuv += "\n• <i>Use /filecrypt to Extract Download Links from FileCrypt URLs</i>"
    tuv += "\n• <i>Use /scrape to Extract Direct Links from Supported Sites</i>"
    tuv += "\n• <i>Use /gd to extract GDrive Links from GDTot, AniDrive, DriveRoot, DriveFlix, IndiDrive, DriveHub, AppDrive, DriveApp, DriveAce, GdFlix, DriveLinks, DriveBit, DriveSharer, DrivePro, HubDrive, KatDrive, Kolop, DriveFire, DriveBuzz, GaDrive, JioDrive, Sharer.pw, Drivehubs & Pahe</i>"
    tuv += "\n\n<b>Made with Love by Miss Emily</b> (https://github.com/missemily2022)"
    await update.reply_text(text=tuv, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.DIRT))
async def dirt(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    is_artstation = is_artstation_link(url)
    if is_artstation:
        link_type = "ArtStation"
        res = direct_link.artstation(url)
    elif "mdisk." in url:
        link_type = "MDisk"
        res = direct_link.mdisk(url)
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
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in bypass_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in scrape_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Site Scraper</b>\n\n<i>Use it with /scrape command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    else:
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b><i>Could not generate Direct Link for your URL</i></b>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    LOGGER.info(f" Received : {cmd} - {link_type} - {url}")
    # log_msg = await update.forward(chat_id=BIN_CHANNEL)
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n<b>Link Type</b> : <i>{link_type}</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    LOGGER.info(f" Destination : {cmd} - {link_type} - {res}")
    if link_type == "GoFile":
        xyz = f"<b><i>Sorry! GoFile Bypass is not supported anymore</i></b>"
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
        xyz = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b><i>Your Telegraph URL(containing Result) is :\n</i></b>{res}"
    else:
        xyz = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b><i>Your Direct-Download Link is :\n</i></b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.BYPS))
async def byps(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    if "droplink." in url or "droplinks." in url:
        link_type = "DropLinks"
        res = bypasser.droplink(url)
    elif "gplink." in url or "gplinks." in url:
        link_type = "GPLinks"
        res = bypasser.gplinks(url)
    elif any(x in url for x in linkvertise_list):
        link_type = "Linkvertise"
        res = bypasser.linkvertise(url)
    elif "adf.ly" in url or "adfly." in url:
        link_type = "AdFly"
        res = bypasser.adfly(url)
    elif "gyanilinks." in url or "gyanilink" in url:
        link_type = "GyaniLinks"
        res = bypasser.gyanilinks(url)
    elif "htpmovies.art/exit.php?url" in url:
        link_type = "HTPMovies GDL"
        res = bypasser.htpmovies(url)
    elif "sirigan.my.id" in url:
        link_type = "Sirigan.my.id"
        res = bypasser.sirigan(url)
    elif "ouo.io" in url or "ouo.press" in url:
        link_type = "Ouo"
        res = bypasser.ouo(url)
    elif any(x in url for x in shst_list):
        link_type = "Shorte.st"
        res = bypasser.shorte(url)
    elif "rocklinks." in url:
        link_type = "RockLinks"
        res = bypasser.rocklinks(url)
    elif "gtlinks." in url:
        link_type = "GTLinks"
        res = bypasser.gtlinks(url)
    elif "gyanilinks." in url:
        link_type = "GyaniLinks"
        res = bypasser.gyanilinks(url)
    elif "shareus." in url:
        link_type = "Shareus"
        res = bypasser.shareus(url)
    elif "shortingly." in url:
        link_type = "Shortingly"
        res = bypasser.shortingly(url)
    elif "tnlink." in url:
        link_type = "TnLink"
        res = bypasser.tnlink(url)
    elif "xpshort." in url:
        link_type = "XpShort"
        res = bypasser.xpshort(url)
    elif "adrinolinks." in url:
        link_type = "AdrinoLinks"
        res = bypasser.adrinolinks(url)
    elif any(x in url for x in yandisk_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in fmed_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in sbembed_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in directdl_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in scrape_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Site Scraper</b>\n\n<i>Use it with /scrape command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    else:
        if url is not None:
            try:
                link_type = "Script Generic"
                res = bypasser.script(url)
            except BaseException:
                err = "<b><i>Could not find Bypass for your URL!</i></b>"
                await update.reply_text(
                    text=err, disable_web_page_preview=True, quote=True
                )
                return
        else:
            err = "<b><i>Could not find your URL!</i></b>"
            await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
            return
    LOGGER.info(f" Received : {cmd} - {link_type} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n<b>Link Type</b> : <i>{link_type}</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    LOGGER.info(f" Destination : {cmd} - {link_type} - {res}")
    xyz = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b><i>Your Bypassed Result is :\n</i></b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.AIO))
async def aio(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.multi_pybyp(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.BIFM))
async def bif(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.bifm(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.DPLK))
async def dpkl(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>DropLinks</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.droplink(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.GPLK))
async def gpkl(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>GPLinks</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.gplinks(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.LINKV))
async def linkv(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Linkvertise</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.linkvertise(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.ADFL))
async def adfl(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>AdFly</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.adfly(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.SRGN))
async def srgn(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Sirigan.my.id</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.sirigan(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.OUOT))
async def ouot(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Ouo</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.ouo(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.SHST))
async def shst(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Shorte.st</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.shorte(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.RKLK))
async def rklk(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>RockLinks</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = bypasser.rocklinks(url)
    LOGGER.info(f" Destination : {cmd} - {res}")
    xyz = f"<b>Bypassed Link :\n</b>{res}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.INDX))
async def indx(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Bhadoo Index</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res = index_scrap(url)
    des_url = telegraph_paste(res)
    time.sleep(5)
    LOGGER.info(f" Destination : {cmd} - {des_url}")
    xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.PSAM))
async def psam(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>PSA</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    """ des_url = psa_scrap(url)
    time.sleep(5)
    LOGGER.info(f" Destination : {cmd} - {des_url}")
    xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}" """
    xyz = "<b>PSA Scraper has been patched for now!</b>"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.FLCY))
async def flcy(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>FileCrypt</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    des_url = filecrypt_scrap(url)
    time.sleep(5)
    LOGGER.info(f" Destination : {cmd} - {des_url}")
    xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.MGNT))
async def mgnt(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Magnet Scraping</i>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    des_url = magnet_scrap(url)
    time.sleep(5)
    LOGGER.info(f" Destination : {cmd} - {des_url}")
    xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.SCRP))
async def scrp(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    if (
        "workers.dev" in url
        or "0:/" in url
        or "1:/" in url
        or "2:/" in url
        or "3:/" in url
        or "4:/" in url
        or "5:/" in url
        or "6:/" in url
    ):
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Bhadoo Index</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        res = index_scrap(url)
        des_url = telegraph_paste(res)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "atishmkv." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>AtishMKV</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = atishmkv_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "cinevez." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Cinevez</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = cinevez_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "cinevood." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Cinevood</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = cinevood_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "filecrypt." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Filecrypt</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = filecrypt_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "htpmovies." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>HTP Movies</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = htpmovies_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "igg-games." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>IGG Games</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = igggames_scrape(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "moviesdrama." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Movies Drama</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = moviesdrama_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "olamovies." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>OlaMovies</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = olamovies_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "psa." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>PSA</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        """ des_url = psa_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}" """
        xyz = "<b>PSA Scraper has been patched for now!</b>"
    elif "toonworld4all." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>ToonWorld4all</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = toonworld4all_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "sharespark." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Sharespark</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = sharespark_scrap(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "privatemoviez." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Privatemoviez</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        des_url = privatemoviez_scrape(url)
        LOGGER.info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}"
    elif "pahe." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Pahe</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        res = pahe(url)
        LOGGER.info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}"
    elif any(x in url for x in yandisk_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in fmed_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in sbembed_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in directdl_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in linkvertise_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    elif any(x in url for x in bypass_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await update.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    else:
        xyz = "This Command does not support this Link!"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.SHRT))
async def shrt(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>"
    await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
    res1 = shortener.bitly(url)
    res2 = shortener.dagd(url)
    res3 = shortener.tinyurl(url)
    res4 = shortener.osdb(url)
    res5 = shortener.ttm(url)
    res6 = shortener.isgd(url)
    res7 = shortener.vgd(url)
    res8 = shortener.clickru(url)
    res9 = shortener.clilp(url)
    LOGGER.info(
        f" Destination : {res1} | {res2} | {res3} | {res4} | {res5} | {res6} | {res7} | {res8} | {res9}"
    )
    xyz = f"<u><b>Shortened URLs :\n\n</b></u>{res1}\n{res2}\n{res3}\n{res4}\n{res5}\n{res6}\n{res7}\n{res8}\n{res9}\n\n<b><i>NOTE:</i></b>\n<i>All the Shortened URLs redirect to the same URL as you entered and all of these links are Ad-Free.</i>"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)


@Client.on_message(filters.command(CMD.GDFS))
async def gdfs(bot, update):
    msg_args = update.text.split(" ", maxsplit=1)
    reply_to = update.reply_to_message
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
    uname = update.from_user.mention
    uid = f"<code>{update.from_user.id}</code>"
    LOGGER.info(f" Received : {cmd} - {url}")
    is_gdtot = is_gdtot_link(url)
    is_drivehubs = is_drivehubs_link(url)
    is_unified = is_unified_link(url)
    is_udrive = is_udrive_link(url)
    is_sharer = is_sharer_link(url)
    if is_gdtot:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>GDTot</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        res = gdtot(url)
        LOGGER.info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}"
    elif is_drivehubs:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>DriveHubs</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        res = drivehubs(url)
        LOGGER.info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}"
    elif is_unified:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>AppDrive Look-Alike</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        res = unified(url)
        LOGGER.info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}"
    elif is_udrive:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>HubDrive Look-Alike</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        res = udrive(url)
        LOGGER.info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}"
    elif is_sharer:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Sharer.pw</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        res = sharerpw(url)
        LOGGER.info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}"
    elif "pahe." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Pahe</i>"
        await update.reply_text(text=abc, disable_web_page_preview=True, quote=True)
        res = pahe(url)
        LOGGER.info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}"
    elif "drive.google.com" in url:
        xyz = "You have entered a Google Drive Link!"
    else:
        xyz = "This Command does not support this Link!"
    await update.reply_text(text=xyz, disable_web_page_preview=True, quote=True)
