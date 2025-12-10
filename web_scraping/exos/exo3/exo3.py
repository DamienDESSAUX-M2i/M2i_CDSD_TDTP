import re
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

DIR_PATH = Path(__file__).parent.resolve()
BASE_URL = "http://books.toscrape.com"


# Question 1
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
}
response = requests.get(url=BASE_URL, headers=headers)


if response.status_code == 200:
    # Question 2
    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.find_all("article", class_="product_pod")
    dataset: list[dict] = []
    for article in articles:
        title = article.find("h3").find("a").get("title")
        price = float(
            re.findall(r"[\d.]+", article.find("p", class_="price_color").get_text())[0]
        )
        match article.find("p", class_="star-rating")["class"][1].lower():
            case "one":
                rating = 1
            case "two":
                rating = 2
            case "three":
                rating = 3
            case "four":
                rating = 4
            case "five":
                rating = 5
            case _:
                rating = 0
        available = (
            "in stock"
            in soup.find("p", class_="instock availability")
            .get_text(strip=True)
            .lower()
        )
        img_url = urljoin(BASE_URL, article.find("img")["src"])
        dataset.append(
            {
                "title": title,
                "price": price,
                "rating": rating,
                "available": available,
                "img_url": img_url,
            }
        )

    # Question 3
    df = pd.DataFrame(dataset)

    # Question 4
    avg_price = df["price"].mean().round(2)
    print("Prix moyenne : ", avg_price)
    max_price = df["price"].max()
    print("Prix maximum : ", max_price)
    min_price = df["price"].min()
    print("Prix minimum : ", min_price)
    group_rating = (
        df.groupby("rating")
        .mean("price")
        .round(2)
        .reset_index()
        .rename(columns={"price": "avg_price"})
        .sort_values("rating", ascending=True)
        .drop("available", axis=1)
    )
    print("Prix moyen par rang :\n", group_rating)

    # Question 5
    csv_path = DIR_PATH / "exo3.csv"
    df.to_csv(path_or_buf=csv_path, index=False)

    # Bonus
    response_img = requests.get(
        url=df.nlargest(n=1, columns="price")["img_url"].iloc[0], headers=headers
    )
    save_path = DIR_PATH / "img.jpg"
    with open(save_path, "wb") as img:
        img.write(response_img.content)
