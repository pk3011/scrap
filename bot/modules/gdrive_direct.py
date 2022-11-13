import base64
import os
import re
from time import sleep
from urllib.parse import parse_qs, urlparse

import chromedriver_autoinstaller
import requests
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bot.config import *


def gdtot(url: str) -> str:
    if GDTOT_CRYPT is None:
        return "GdTot Crypt not provided!"
    crypt = GDTOT_CRYPT
    client = requests.Session()
    match = re.findall(r"https?://(.+)\.gdtot\.(.+)\/\S+\/\S+", url)[0]
    client.cookies.update({"crypt": crypt})
    res = client.get(url)
    res = client.get(f"https://{match[0]}.gdtot.{match[1]}/dld?id={url.split('/')[-1]}")
    url = re.findall(r'URL=(.*?)"', res.text)[0]
    info = {}
    info["error"] = False
    params = parse_qs(urlparse(url).query)
    if "gd" not in params or not params["gd"] or params["gd"][0] == "false":
        info["error"] = True
        if "msgx" in params:
            info["message"] = params["msgx"][0]
        else:
            info["message"] = "Invalid link"
    else:
        decoded_id = base64.b64decode(str(params["gd"][0])).decode("utf-8")
        drive_link = f"https://drive.google.com/open?id={decoded_id}"
        info["gdrive_link"] = drive_link
    if not info["error"]:
        return info["gdrive_link"]
    else:
        return f"{info['message']}"


def unified(url: str) -> str:
    if (UNIFIED_EMAIL or UNIFIED_PASS) is None:
        return "AppDrive Look-Alike Credentials not Found!"
    try:
        account = {"email": UNIFIED_EMAIL, "passwd": UNIFIED_PASS}
        client = requests.Session()
        client.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
            }
        )
        data = {"email": account["email"], "password": account["passwd"]}
        client.post(f"https://{urlparse(url).netloc}/login", data=data)
        res = client.get(url)
        key = re.findall('"key",\s+"(.*?)"', res.text)[0]
        ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
        info = re.findall(">(.*?)<\/li>", res.text)
        info_parsed = {}
        for item in info:
            kv = [s.strip() for s in item.split(":", maxsplit=1)]
            info_parsed[kv[0].lower()] = kv[1]
        info_parsed = info_parsed
        info_parsed["error"] = False
        info_parsed["link_type"] = "login"
        headers = {
            "Content-Type": f"multipart/form-data; boundary={'-' * 4}_",
        }
        data = {"type": 1, "key": key, "action": "original"}
        if len(ddl_btn):
            info_parsed["link_type"] = "direct"
            data["action"] = "direct"
        while data["type"] <= 3:
            boundary = f'{"-" * 6}_'
            data_string = ""
            for item in data:
                data_string += f"{boundary}\r\n"
                data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
            data_string += f"{boundary}--\r\n"
            gen_payload = data_string
            try:
                response = client.post(url, data=gen_payload, headers=headers).json()
                break
            except BaseException:
                data["type"] += 1
        if "url" in response:
            info_parsed["gdrive_link"] = response["url"]
        elif "error" in response and response["error"]:
            info_parsed["error"] = True
            info_parsed["error_message"] = response["message"]
        else:
            info_parsed["error"] = True
            info_parsed["error_message"] = "Something went wrong :("
        if info_parsed["error"]:
            return info_parsed
        info_parsed["src_url"] = url
        if "appdrive." in urlparse(url).netloc:
            flink = info_parsed["gdrive_link"]
            return flink
        elif urlparse(url).netloc in (
            "driveapp.in",
            "drivehub.in",
            "gdflix.pro",
            "drivesharer.in",
            "drivebit.in",
            "drivelinks.in",
            "driveace.in",
            "drivepro.in",
            "gdflix.top",
        ):
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            flink = drive_link
            return flink
        else:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn btn-primary')]/@href"
            )[0]
            flink = drive_link
            return flink
    except Exception as err:
        return f"Encountered Error while parsing Link : {err}"


def udrive(url: str) -> str:
    client = requests.Session()
    if "hubdrive." in url:
        url = url.replace(".me", ".pw")
        if HUBDRIVE_CRYPT is None:
            return "HubDrive Crypt not provided!"
        client.cookies.update({"crypt": HUBDRIVE_CRYPT})
    if "katdrive." in url:
        if KATDRIVE_CRYPT is None:
            return "KatDrive Crypt not provided!"
        client.cookies.update({"crypt": KATDRIVE_CRYPT})
    if "kolop." in url:
        if KOLOP_CRYPT is None:
            return "Kolop Crypt not provided!"
        client.cookies.update({"crypt": KOLOP_CRYPT})
    if "drivefire." in url:
        if DRIVEFIRE_CRYPT is None:
            return "DriveFire Crypt not provided!"
        client.cookies.update({"crypt": DRIVEFIRE_CRYPT})
    if "drivebuzz." in url:
        if DRIVEBUZZ_CRYPT is None:
            return "DriveBuzz Crypt not provided!"
        client.cookies.update({"crypt": DRIVEBUZZ_CRYPT})
    if "drivehub." in url:
        if DRIVEHUB_CRYPT is None:
            return "DriveHub Crypt not provided!"
        client.cookies.update({"crypt": DRIVEHUB_CRYPT})
    if "gadrive." in url:
        if GADRIVE_CRYPT is None:
            return "GaDrive Crypt not provided!"
        client.cookies.update({"crypt": GADRIVE_CRYPT})
    if "jiodrive." in url:
        if JIODRIVE_CRYPT is None:
            return "JioDrive Crypt not provided!"
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
    if "drivefire." in url:
        gd_id = res.rsplit("/", 1)[-1]
        flink = f"https://drive.google.com/file/d/{gd_id}"
        return flink
    elif "drivehub." in url:
        gd_id = res.rsplit("=", 1)[-1]
        flink = f"https://drive.google.com/open?id={gd_id}"
        return flink
    elif "drivebuzz." in url:
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
    if "drivebuzz." in url:
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


def sharerpw(url: str, forced_login=False) -> str:
    if (Sharerpw_XSRF or Sharerpw_laravel) is None:
        return "Sharerpw Cookies not Found!"
    try:
        scraper = requests.Session()
        scraper.cookies.update(
            {
                "XSRF-TOKEN": Sharerpw_XSRF,
                "laravel_session": Sharerpw_laravel,
            }
        )
        res = scraper.get(url)
        token = re.findall("_token\s=\s'(.*?)'", res.text, re.DOTALL)[0]
        ddl_btn = etree.HTML(res.content).xpath("//button[@id='btndirect']")
        info_parsed = parse_info(res, url)
        info_parsed["error"] = True
        info_parsed["src_url"] = url
        info_parsed["link_type"] = "login"
        info_parsed["forced_login"] = forced_login
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
        }
        data = {"_token": token}
        if len(ddl_btn):
            info_parsed["link_type"] = "direct"
        if not forced_login:
            data["nl"] = 1
        try:
            res = scraper.post(url + "/dl", headers=headers, data=data).json()
        except BaseException:
            return info_parsed
        if "url" in res and res["url"]:
            info_parsed["error"] = False
            info_parsed["gdrive_link"] = res["url"]
        if len(ddl_btn) and not forced_login and "url" not in info_parsed:
            return sharerpw(url, forced_login=True)
        return info_parsed["gdrive_link"]
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
