import requests


def get_full_url(url: str):
    response = requests.head(url)
    if response.status_code == 302:
        return response.headers["location"]
    return None


url = "https://upflix.pl/r/apEf24"
print(get_full_url(url))