import json
import time
import urllib.parse
from base64 import b64decode

import cloudscraper

from bot.helpers.functions import api_checker

next_page = False
next_page_token = ""


def index_scraper(payload, url):
    global next_page
    global next_page_token
    url = url + "/" if url[-1] != "/" else url
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.post(url, data=payload)
    time.sleep(1)
    if resp.status_code == 401:
        return "Could not Access your Entered URL!"
    try:
        resp2 = json.loads(b64decode(resp.text[::-1][24:-20]).decode("utf-8"))
    except BaseException:
        return "Something Went Wrong!"
    page_token = resp2["nextPageToken"]
    if page_token is None:
        next_page = False
    else:
        next_page = True
        next_page_token = page_token
    res = ""
    if list(resp2.get("data").keys())[0] == "error":
        pass
    else:
        file_len = len(resp2["data"]["files"])
        time.sleep(1)
        for i, _ in enumerate(range(file_len)):
            file_type = resp2["data"]["files"][i]["mimeType"]
            file_name = resp2["data"]["files"][i]["name"]
            if file_type == "application/vnd.google-apps.folder":
                pass
            else:
                ddl = url + urllib.parse.quote(file_name)
                res += f"• <b>{file_name}</b>:-<br><code>{ddl}</code><br><br>"
        return res


def index_scrap(url):
    x = 0
    payload = {"page_token": next_page_token, "page_index": x}
    msg = f"Index Link: {url}\n\n"
    msg += index_scraper(payload, url)
    while next_page:
        payload = {"page_token": next_page_token, "page_index": x}
        time.sleep(2)
        msg += index_scraper(payload, url)
        x += 1
    return msg


def atishmkv_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "atishmkv_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def cinevez_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "cinevez_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def cinevood_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "cinevood_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def filecrypt_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "filecrypt_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def htpmovies_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "htpmovies_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def igggames_scrape(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "igggames_scrape", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def moviesdrama_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "moviesdrama_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def privatemoviez_scrape(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "privatemoviez_scrape", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def magnet_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "magnet_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def sharespark_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "sharespark_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def olamovies_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "olamovies_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def psa_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.get(api, json={"type": "psa_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def toonworld4all_scrap(url):
    dom = api_checker()
    api = f"{dom}/scraper"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "toonworld4all_scrap", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]
