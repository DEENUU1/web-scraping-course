import httpx
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


PROXY_AUTH_KEY = os.getenv("PROXY_AUTH")
PROXY_URL = f"http://{PROXY_AUTH_KEY}@smartproxy.crawlbase.com:8012"
PROXIES = {
    "http://": PROXY_URL,
    "https://": PROXY_URL
}

url = "https://upflix.pl/serial/zobacz/selection-day-2018"


def get_content(url: str):
    response = httpx.get(
        url, proxies=PROXIES, verify=False
    )
    return response.text


def get_title(content):
    soup = BeautifulSoup(content, "html.parser")
    title = soup.find("h1")
    if title:
        return title.text
    return None


content = get_content(url)
print(get_title(content))

