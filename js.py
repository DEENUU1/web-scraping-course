#  -> https://www.imdb.com/title/tt0983514/

import requests

full_url = requests.get("https://www.upflix.pl/r/kmuXjK").url
print(full_url)