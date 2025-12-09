import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DIR_PATH = Path(__file__).parent.resolve()
BASE_URL = "http://quotes.toscrape.com"


def get_response(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
    }
    return requests.get(url=url, headers=headers)


def transform_data(soup):
    citations = soup.find_all("div", class_="quote")
    data_transformed = []
    for citation in citations:
        data = {}
        data["text"] = (
            citation.find("span", class_="text")
            .string.replace("“", "")
            .replace("”", "")
        )
        data["author"] = citation.find(class_="author").string
        data["tags"] = [tag.string for tag in citation.find_all("a", class_="tag")]
        data_transformed.append(data)
    return data_transformed


def get_dataset(url, max_deph: int):
    dataset = []

    url_temp = url
    iter_deph = 1
    while iter_deph <= max_deph:
        response = get_response(url=url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            data_transformed = transform_data(soup=soup)
            dataset.extend(data_transformed)
            try:
                a = soup.select(".next a")[0]
                href = a["href"]
                url = url_temp + href
            except Exception:
                break
        time.sleep(1)
        iter_deph += 1

    return dataset


def save(json_path, dataset) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)


def main():
    dataset = get_dataset(url=BASE_URL, max_deph=3)
    json_path = DIR_PATH / "exo2.json"
    save(json_path=json_path, dataset=dataset)


if __name__ == "__main__":
    main()
