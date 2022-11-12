import os
import re
from time import sleep
from urllib.parse import urlparse

import chromedriver_autoinstaller
import cloudscraper
import requests
from PyBypass import bypass as gd_dir
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bot.config import *


def gdtot(url: str) -> str:
    crypt = GDTOT_CRYPT
    if crypt is None:
        return "GdTot Crypt not provided"
    try:
        gd_link = gd_dir(url, gdtot_crypt=crypt)
        return gd_link
    except Exception as err:
        return f"Encountered Error while parsing Link : {err}"


def unified(url: str) -> str:
    if (UNIFIED_EMAIL or UNIFIED_PASS) is None:
        return "AppDrive Look-Alike Credentials not Found!"
    try:
        gd_link = gd_dir(
            url, appdrive_email=UNIFIED_EMAIL, appdrive_password=UNIFIED_PASS
        )
        return gd_link
    except Exception as err:
        return f"Encountered Error while parsing Link : {err}"


def udrive(url: str) -> str:
    if "hubdrive" or "katdrive" in url:
        client = requests.Session()
    else:
        client = cloudscraper.create_scraper(delay=10, browser="chrome")
    if "hubdrive" in url:
        if "hubdrive.in" in url:
            url = url.replace(".in", ".pro")
        client.cookies.update({"crypt": HUBDRIVE_CRYPT})
    if "katdrive" in url:
        client.cookies.update({"crypt": KATDRIVE_CRYPT})
    if "kolop" in url:
        client.cookies.update({"crypt": KOLOP_CRYPT})
    if "drivefire" in url:
        client.cookies.update({"crypt": DRIVEFIRE_CRYPT})
    if "drivebuzz" in url:
        client.cookies.update({"crypt": DRIVEBUZZ_CRYPT})
    if "gadrive" in url:
        client.cookies.update({"crypt": GADRIVE_CRYPT})
    if "jiodrive" in url:
        client.cookies.update({"crypt": JIODRIVE_CRYPT})
    res = client.get(url)
    info_parsed = parse_info(res, url)
    info_parsed["error"] = False
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    file_id = url.split("/")[-1]
    data = {"id": file_id}
    headers = {"x-requested-with": "XMLHttpRequest"}
    try:
        res = client.post(req_url, headers=headers, data=data).json()["file"]
    except BaseException:
        return "File Not Found or User rate exceeded !!"
    if "drivefire" in url:
        gd_id = res.rsplit("/", 1)[-1]
        flink = f"https://drive.google.com/file/d/{gd_id}"
        return flink
    elif "drivehub" in url:
        gd_id = res.rsplit("=", 1)[-1]
        flink = f"https://drive.google.com/open?id={gd_id}"
        return flink
    elif "drivebuzz" in url:
        gd_id = res.rsplit("=", 1)[-1]
        flink = f"https://drive.google.com/open?id={gd_id}"
        return flink
    else:
        try:
            gd_id = re.findall("gd=(.*)", res, re.DOTALL)[0]
        except BaseException:
            return "Unknown Error Occurred!"
        flink = f"https://drive.google.com/open?id={gd_id}"
        return flink


def parse_info(res, url):
    info_parsed = {}
    if "drivebuzz" in url:
        info_chunks = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
    elif "sharer.pw" in url:
        f = re.findall(">(.*?)<\/td>", res.text)
        info_parsed = {}
        for i in range(0, len(f), 3):
            info_parsed[f[i].lower().replace(" ", "_")] = f[i + 2]
        return info_parsed
    else:
        info_chunks = re.findall(">(.*?)<\/td>", res.text)
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i + 1]
    return info_parsed


def sharerpw(url: str) -> str:
    if Sharerpw_XSRF is None or Sharerpw_laravel is None:
        return "Sharerpw Cookies not Found!"
    try:
        gd_link = gd_dir(
            url,
            sharerpw_xsrf_token=Sharerpw_XSRF,
            sharerpw_laravel_session=Sharerpw_laravel,
        )
        return gd_link
    except Exception as err:
        return f"Encountered Error while parsing Link : {err}"


def drivehubs(url: str) -> str:
    chromedriver_autoinstaller.install()

    os.chmod("/usr/src/app/chromedriver", 755)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    wd = webdriver.Chrome("/usr/src/app/chromedriver", chrome_options=chrome_options)
    wd.get(url)
    wd.find_element(By.XPATH, '//button[@id="fast"]').click()
    sleep(10)
    wd.switch_to.window(wd.window_handles[-1])
    flink = wd.current_url
    wd.close()
    if "drive.google.com" in flink:
        return flink
    else:
        return f"ERROR! Maybe Direct Download is not working for this file !\n Retrived URL : {flink}"


def pahe(url: str) -> str:
    chromedriver_autoinstaller.install()

    AGREE_BUTTON = "//*[contains(text(), 'AGREE')]"
    LINK_TYPE = ["//*[contains(text(), 'GD')]"]
    GENERATE = "#generater > img"
    SHOW_LINK = "showlink"
    CONTINUE = "Continue"

    os.chmod("/usr/src/app/chromedriver", 755)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    wd = webdriver.Chrome("/usr/src/app/chromedriver", chrome_options=chrome_options)
    wd.get(url)
    texts = [
        y for x in [wd.find_elements("xpath", type) for type in LINK_TYPE] for y in x
    ]
    texts[1].click()
    if "intercelestial." not in wd.current_url:
        wd.close()
        wd.switch_to(wd.find_all(wd.switch_to.Window())[0])
        LOGGER(__name__).info("Chrome Pahe: Website Switched!")
    try:
        WebDriverWait(wd, 10).until(
            ec.element_to_be_clickable((By.XPATH, AGREE_BUTTON))
        ).click()
    except TimeoutException:
        LOGGER(__name__).info("Chrome Pahe: Browser Verification Error!")
        return "Chrome Pahe: Browser Verification Error!"
    wd.execute_script("document.getElementById('landing').submit();")
    WebDriverWait(wd, 30).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, GENERATE))
    ).click()
    WebDriverWait(wd, 45).until(ec.element_to_be_clickable((By.ID, SHOW_LINK))).click()
    window_after = wd.window_handles[1]
    wd.switch_to.window(window_after)
    wd.execute_script("window.scrollTo(0,535.3499755859375)")
    WebDriverWait(wd, 30).until(ec.element_to_be_clickable((By.LINK_TEXT, CONTINUE)))
    last = wd.find_element("link text", CONTINUE)
    sleep(5)
    wd.execute_script("arguments[0].click();", last)
    flink = wd.current_url
    wd.close()
    gd_url = gdtot(flink)
    return gd_url
