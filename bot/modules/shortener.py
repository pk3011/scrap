import cloudscraper
import requests

from bot.helpers.functions import api_checker


def bitly(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "bitly_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def dagd(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "dagd_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def tinyurl(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "tinyurl_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def osdb(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "osdb_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def ttm(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "ttm_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def isgd(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "isgd_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def vgd(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "vgd_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def clickru(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "clckru_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


def clilp(url):
    dom = api_checker()
    api = f"{dom}/shorten"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "clilp_shorten", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]
