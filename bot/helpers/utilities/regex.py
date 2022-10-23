import re


def is_a_url(url: str):
    url = re.match(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", url)
    return bool(url)


def is_gdtot_link(url: str):
    url = re.match(r"https?://.+\.gdtot\.\S+", url)
    return bool(url)


def is_unified_link(url: str):
    url = re.match(
        r"https?://(anidrive|driveroot|driveflix|indidrive|drivehub|appdrive|driveapp|driveace|gdflix|drivelinks|drivebit|drivesharer|drivepro)\.\S+",
        url,
    )
    return bool(url)


def is_udrive_link(url: str):
    url = re.match(
        r"https?://(hubdrive|katdrive|kolop|drivefire|drivebuzz|gadrive|jiodrive)\.\S+",
        url,
    )
    return bool(url)


def is_sharer_link(url: str):
    url = re.match(r"https?://(sharer)\.pw/\S+", url)
    return bool(url)


def is_drivehubs_link(url: str):
    return "drivehubs." in url


def is_artstation_link(url: str):
    url = re.match(r"artstation\.com/(?:artwork|projects)/([0-9a-zA-Z]+)", url)
    return bool(url)


def is_sendcm_folder_link(url: str):
    return (
        "https://send.cm/s/" in url
        or "https://send.cm/?sort" in url
        or "https://send.cm/?sort_field" in url
        or "https://send.cm/?sort_order" in url
    )
