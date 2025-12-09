import logging

import pandas as pd
import requests


class ResponsesTransformer:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def transform(
        self, responses: list[requests.Response]
    ) -> tuple[list[str], pd.DataFrame]:
        try:
            self.logger.info("Get HTML")
            responses_html = [r.text for r in responses]
            self.logger.info("\tSuccess")

            self.logger.info("Create DataFrame")
            data = {"url": [], "statut_HTTP": [], "taille": [], "temps_reponse": []}
            nb_characters = [len(r_html) for r_html in [r.text for r in responses]]
            for r, r_nb_characters in zip(responses, nb_characters):
                data["url"].append(r.url)
                data["statut_HTTP"].append(r.status_code)
                data["taille"].append(r_nb_characters)
                data["temps_reponse"].append(r.elapsed.total_seconds())
            df = pd.DataFrame(data)
            self.logger.info("\tSuccess")

            return (responses_html, df)
        except Exception as e:
            self.logger.error(f"Responses transformer - error : {e}")
            raise
