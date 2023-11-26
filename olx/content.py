from typing import Optional
import requests
import json


class GetOlxContent:

    def __init__(self):
        self.main_url = "https://www.olx.pl/api/v1/offers/?offset=40&limit=40&category_id=15&region_id=2&city_id=17871&filter_refiners=spell_checker&sl=18ae25cfa80x3938008f"
        self.total = 0

    def fetch_content(self):
        while self.main_url:
            try:
                response = requests.get(self.main_url)
                if response.status_code == 200:
                    json_data = json.loads(response.content)
                    if not json_data:
                        break

                    self.save_to_json(json_data, f"olx_data_{self.total}.json")

                    self.main_url = self.get_next_page_url(json_data)
                    self.total += 1

            except Exception as e:
                print(e)

    @staticmethod
    def save_to_json(json_data, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4)

    @staticmethod
    def get_next_page_url(json_data) -> Optional[str]:
        links = json_data.get("links")
        if links:
            next_page = links.get("next")
            if next_page:
                return next_page.get("href")

        return None


scraper = GetOlxContent()
scraper.fetch_content()