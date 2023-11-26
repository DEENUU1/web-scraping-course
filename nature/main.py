from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from typing import Optional, List



def get_html(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    return None


def get_max_page(soup):
    result = []

    pagination_items = soup.find_all("a", class_="c-pagination__link")
    for element in pagination_items:
        text = element.text.replace("page", "").replace("Next", "").replace("\n", "").strip()
        try:
            result.append(int(text))
        except Exception as e:
            continue

    return max(result)


def get_all_articles(soup):
    articles = None

    container = soup.find("ul", class_="ma0 mb-negative-2 clean-list")
    if container:
        articles = container.find_all("li")

    return articles

@dataclass
class Article:
    title: str
    type: str
    date: str
    url: str
    authors: List[Optional[str]] = None
    short_desc: str = None


def get_article_data(article):
    short_desc = None

    title_container = article.find("a", class_="text-gray")
    type_container = article.find("span", {"data-test": "article.type"})
    desc_container = article.find("div", {"itemprop": "description"})
    date_container = article.find("time")
    authors_container = article.find("ul", {"data-test": "author-list"})

    authors = []
    if authors_container:
        author_name = authors_container.find_all("span", {"itemprop": "name"})
        for name in author_name:
            authors.append(name.text)

    if desc_container:
        short_desc = desc_container.find("p")
        if short_desc:
            short_desc = short_desc.text

    if not title_container and not type_container and not date_container:
        return None

    return Article(
        title=title_container.text.strip(),
        type=type_container.text,
        url=title_container["href"],
        date=date_container["datetime"],
        authors=authors,
        short_desc=short_desc
    )


def main():
    SUBJECTS = ["physical-sciences", "earth-and-environmental-sciences", "biological-sciences", "health-sciences",
                "scientific-community-and-society"]

    for subject in SUBJECTS:
        url = f"https://www.nature.com/subjects/{subject}/nature?searchType=journalSearch&sort=PubDate&page="
        url_max_page = f"https://www.nature.com/subjects/{subject}/nature"
        content_maxpage = get_html(url_max_page)
        max_page = get_max_page(content_maxpage)

        for i in range(1, max_page + 1):
            content = get_html(f"{url}{i}")
            all_articles = get_all_articles(content)
            for article in all_articles:
                article_details = get_article_data(article)
                if article_details:
                    print(article_details)
                    print("\n\n")

main()