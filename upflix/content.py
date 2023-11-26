import requests
from bs4 import BeautifulSoup


URLS = ["https://upflix.pl/sitemap.xml?page=2"]


def get_content(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

    return None


def get_soup(content):
    return BeautifulSoup(content, "lxml")

def get_type(url: str):
    if "film" in url:
        return "Film"
    if "serial" in url:
        return "Serial"


def get_year(url: str):
    return url[-4:]

def parse():
    data = []

    for url in URLS:
        content = get_content(url)
        if not content:
            continue

        soup = get_soup(content)
        elements = soup.find_all("url")

        for element in elements:
            el = {}
            loc = element.find("loc").text
            mod = element.find("lastmod").text

            if "/zobacz/" in loc:
                el["url"] = loc
                el["mod"] = mod
                el["type"] = get_type(loc)
                el["year"] = get_year(loc)

                data.append(el)

    return data


print(parse())