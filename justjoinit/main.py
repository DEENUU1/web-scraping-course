from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple
from repository import create_content, get_all


class GetContent():
    def __init__(self, category: str):
        self.url = f"https://justjoin.it/all-lactions/{category}"
        self.category = category
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.data = []
        self.pixels_to_scroll = "500"

    def fetch_content(self) -> None:
        try:
            last_height = 0
            while True:
                elements = self.driver.find_elements(By.CLASS_NAME, "css-2crog7")
                if elements:
                    for element in elements:
                        self.data.append(
                            element.get_attribute("outerHTML")
                        )
                self.driver.execute_script(
                    f"window.scrollBy(0, {self.pixels_to_scroll});"
                )
                time.sleep(1)

                new_height = self.driver.execute_script("return window.scrollY")
                if new_height == last_height:
                    break
                last_height = new_height

        except Exception as e:
            print(e)

        finally:
            self.driver.quit()

    def save_data(self) -> None:
        for data in self.data:
            create_content(data)


class Parser():
    def __init__(self):
        self.parsed_data = {}

    def parse_html(self, html: Optional[str]) -> None:
        soup = BeautifulSoup(html, "html.parser")

        title_element = soup.find("h2", class_="css-16gpjqw")
        url_element = soup.find("a", class_="css-4lqp8g")
        salary_element = soup.find("div", class_="css-1b2ga3v")
        skills_element = soup.find("div", class_="css-yicj0q")
        company_name_div = soup.find("div", class_="css-ldh1c9")
        company_logo = soup.find("img")
        localization_element = soup.find("span", class_="css-1o4wo1x")

        if title_element:
            self.parsed_data["title"] = title_element.text
        if url_element:
            self.parsed_data["url"] = url_element["href"]
        if salary_element:
            self.parsed_data["salary"] = salary_element.text
        if skills_element:
            self.parsed_data["skills"] = [skill.text for skill in skills_element]
        if company_name_div:
            company_name = company_name_div.find("span")
            if company_name:
                self.parsed_data["company_name"] = company_name.text
        if company_logo:
            self.parsed_data["logo"] = company_logo["src"]
        if localization_element:
            self.parsed_data["localization"] = localization_element.text


CATEGORIES = [
    # "javascript",
    # "html",
    # "php",
    # "ruby",
    # "java",
    # "net",
    # "scala",
    # "c",
    # "mobile",
    # "testing",
    # "devops",
    # "admin",
    # "ux",
    # "pm",
    # "game",
    # "analytics",
    # "security",
    # "data",
    "go",
    # "support",
    # "erp",
    # "architecture",
    # "other",
]


def run():
    try:
        for category in CATEGORIES:
            scraper = GetContent(category)
            scraper.fetch_content()
            scraper.save_data()


        page_content = get_all()
        for content in page_content:
            proces = Parser()
            proces.parse_html(content.content)
            print(proces.parsed_data)

    except Exception as e:
        print(e)



run()