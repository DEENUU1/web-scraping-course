from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.options import Options

load_dotenv()

SESSION_ID = os.getenv("INSTAGRAM_SESSIONID")


class Scraper:

    @staticmethod
    def _chrome_driver_conf() -> Options:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument(
            "--disable-features=IsolateOrigins,site-per-process"
        )
        chrome_options.add_argument(
            "--enable-features=NetworkService,NetworkServiceInProcess"
        )
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return chrome_options


def scroll(driver, callback) -> None:
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        consecutive_scrolls = 0

        while consecutive_scrolls < 3:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                consecutive_scrolls += 1
            else:
                consecutive_scrolls = 0

            last_height = new_height
            callback(driver)

    except Exception as e:
        print(e)


class InstagramScraper(Scraper):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id
        self._driver = webdriver.Chrome(options=self._chrome_driver_conf())
        self.url = f"https://www.instagram.com/{self.user_id}/"
        self._driver.get(self.url)
        self._driver.add_cookie(
            {
                "name": "sessionid",
                "value": SESSION_ID,
                "domain": ".instagram.com"
            }
        )
        self._driver.refresh()

    def extract_images(self):
        extracted_images = []

        try:

            def extract_callback(driver):
                img_elements = self._driver.find_elements(
                    By.CLASS_NAME,
                    "x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3"
                )
                for image in img_elements:
                    src_attribute = image.get_attribute("src")
                    if src_attribute and src_attribute not in extracted_images:
                        print(src_attribute)
                        extracted_images.append(src_attribute)

            scroll(self._driver, extract_callback)

        except Exception as e:
            print(e)

    def run(self):
        try:
            self.extract_images()
        except Exception as e:
            print(e)

        finally:
            self._driver.quit()


scraper = InstagramScraper("sawardega_wataha")
scraper.run()
