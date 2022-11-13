from re import search
from time import sleep, time
from bs4 import BeautifulSoup
from requests import get as rget

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import *
from bot.logging import LOGGER
from bot.modules.regex import *
from bot.helpers.decorators import user_commands
from bot.helpers.functions import get_readable_time
from bot.modules.pasting import telegraph_paste

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


prefixes = COMMAND_PREFIXES
commands = ["mkvcinema", f"mkvcinema@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def bypass(_, message: Message):
    """
    Scrape MKV Cinemas URL for Direct Links
    """
    global temp
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
    msg_text = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Processing your URL.....</b>"
    LOGGER(__name__).info(f" Received : {cmd} - {url}")
    msg = await message.reply_text(
        text=msg_text, disable_web_page_preview=True, quote=True
    )
    sleep(2)
    abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n<b>Link Type</b> : <i>MKVCinemas</i>"
    await msg.edit(text=abc)
    try:
        soup = BeautifulSoup(rget(url).content, 'html.parser')
        links = []
        for link in soup.find_all('a', class_="gdlink"):
            links.append(link.get('href'))

        for link in soup.find_all('a', class_="button"):
            links.append(link.get('href'))

        melob_links = []
        count = -1
        for l in links:
            count += 1
            id = BeautifulSoup(rget(links[count]).content, 'html.parser').find_all("input")[1]['value']
            link = f'https://www.mealob.com{id}'
            melob_links.append(link)
        melob_count = len(melob_links)
        wait_time = get_readable_time(len(melob_links) * 23)
        melob_msg = f"Found {melob_count} Links to be scrapped in your MkvCinema link. It'll take around {wait_time} to finish the process. Please wait..."
        temp = await message.reply_text(
            text=melob_msg, disable_web_page_preview=True, quote=True
        )
    except Exception as err:
        await temp.delete()
        err_msg = f"Error Ocuured : {err}"
        await msg.edit(text=err_msg)
        return

    bypassed_links = []
    failed_links = []
    chromedriver_autoinstaller.install()
    for link in melob_links:
        generater = '//*[@id="generater"]'
        showlink = '//*[@id="showlink"]'
        landing = '//*[@id="landing"]/div[2]/center/img'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        wd = webdriver.Chrome(options=chrome_options)
        try:
            wd.get(link)
            sleep(3)
            WebDriverWait(wd, 10).until(ec.element_to_be_clickable((By.XPATH, landing))).click()
            WebDriverWait(wd, 10).until(ec.element_to_be_clickable((By.XPATH, generater))).click()
            WebDriverWait(wd, 10).until(ec.element_to_be_clickable((By.XPATH, showlink))).click()
            wd.current_window_handle
            IItab = wd.window_handles[1]
            wd.switch_to.window(IItab)
            LOGGER(__name__).info(f'Bypassed Link: {cmd} - {wd.current_url}')
            bypassed_links.append(wd.current_url)
        except Exception as err:
            LOGGER(__name__).error(f'MKVCinema Melob Error: {err}')
            failed_links.append(link)
    if len(failed_links) == melob_count:
        await temp.delete()
        err = "Scrapping has failed!"
        await msg.edit(text=err)
        return

    bypassed_msg = ""
    for bypsd_link in bypassed_links:
        bypassed_msg += f'• <code>{bypsd_link}</code><br>>'
    tlg_url = telegraph_paste(bypassed_msg)
    timelog = get_readable_time(time() - start)
    final = f'Bypassed Result(via Telegraph): \n{tlg_url}\nTime Taken: {timelog}'
    await msg.edit(text=final)
