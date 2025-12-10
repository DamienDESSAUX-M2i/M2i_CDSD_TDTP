import logging
from collections import Counter
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup


class ResponsesTransformer:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def transform(self, responses: list[requests.Response]) -> dict[str, pd.DataFrame]:
        dataset = self._get_dataset(responses=responses)
        return self._get_dataframes(dataset=dataset)

    def stats(
        self, dict_dataframes: dict[str, pd.DataFrame]
    ) -> dict[str, pd.DataFrame]:
        try:
            self.logger.info("Attempting to create statistics")

            df_authors = dict_dataframes["df_authors"]
            top5_authors = df_authors.nlargest(n=5, columns="nb_occurrences")

            df_tags = dict_dataframes["df_tags"]
            top10_tags = df_tags.nlargest(n=10, columns="nb_occurrences")

            df_citations = dict_dataframes["df_citations"]
            df_citations["length"] = df_citations["text"].str.len()
            mean_length_citations = pd.DataFrame(
                {"mean_length_citations": [df_citations["length"].mean().round(2)]}
            )

            self.logger.info("\tSuccess")

            return {
                "top5_authors": top5_authors,
                "top10_tags": top10_tags,
                "mean_length_citations": mean_length_citations,
            }
        except Exception as e:
            self.logger.error(f"Responses transformer - error : {e}")

    def _get_dataframes(self, dataset: list[dict[str, Any]]) -> dict[str, pd.DataFrame]:
        try:
            self.logger.info("Attempting to create dataframes")
            df_citations = pd.DataFrame(
                [{"author": data["author"], "text": data["text"]} for data in dataset]
            )
            df_authors = pd.DataFrame(
                [
                    {"author": k, "nb_occurrences": v}
                    for k, v in dict(
                        Counter([data["author"] for data in dataset])
                    ).items()
                ]
            )
            df_tags = pd.DataFrame(
                [
                    {"tag": k, "nb_occurrences": v}
                    for k, v in dict(
                        Counter([tag for data in dataset for tag in data["tags"]])
                    ).items()
                ]
            )
            self.logger.info("\tSuccess")
            return {
                "df_citations": df_citations,
                "df_authors": df_authors,
                "df_tags": df_tags,
            }
        except Exception as e:
            self.logger.error(f"Responses transformer - error : {e}")

    def _get_dataset(self, responses: list[requests.Response]) -> list[dict[str, Any]]:
        try:
            self.logger.info("Attempting to create dataset")
            dataset: list[dict[str, Any]] = []
            for response in responses:
                soup = BeautifulSoup(response.text, "lxml")
                quotes = soup.find_all("div", class_="quote")
                for quote in quotes:
                    text = quote.find(class_="text").text
                    author = quote.find(class_="author").text
                    tags = [tag.text for tag in quote.find_all(class_="tag")]
                    author_url = soup.select(".author + a")[0].get("href")
                    dataset.append(
                        {
                            "text": text,
                            "author": author,
                            "tags": tags,
                            "author_url": author_url,
                        }
                    )
            self.logger.info("\tSuccess")
            return dataset
        except Exception as e:
            self.logger.error(f"Responses transformer - error : {e}")
            raise
