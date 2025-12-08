import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout
from requests.packages.urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
DIR_PATH = Path(__file__).parent.resolve()


def get_session() -> requests.Session:
    retry_strategy = Retry(
        total=1,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("http://", adapter=adapter)
    session.mount("https://", adapter=adapter)

    return session


def request_get(
    session: requests.Session, url: str, params: dict[str, Any]
) -> Any | None:
    try:
        response = session.get(url=url, params=params)
        return response.json()
    except Timeout:
        print("Timeout")
    except ConnectionError:
        print("Connexion error")
    except HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Code: {response.status_code}")
        print(f"Message: {response.text}")
    except RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


def get_dataset(
    session: requests.Session, url: str, params: dict[str, Any], villes: list[str]
) -> list[Any]:
    dataset = []
    for ville in villes:
        params["q"] = ville
        data = request_get(session=session, url=url, params=params)
        if data:
            data["name"] = ville
            dataset.append(data)
    return dataset


def create_csv(csv_path: Path, villes: list[str]) -> None:
    endpoint = "weather"
    url = "/".join([BASE_URL, endpoint])
    params = {"q": "", "appid": API_KEY, "units": "metric", "lang": "fr"}
    session = get_session()
    dataset = get_dataset(session=session, url=url, params=params, villes=villes)

    save_dataset(csv_path=csv_path, dataset=dataset)


def save_dataset(csv_path: Path, dataset: dict[str, Any]) -> None:
    dict_data = {
        "name": [],
        "temp": [],
        "feels_like": [],
        "humidity": [],
        "description": [],
    }
    for data in dataset:
        dict_data["name"].append(data["name"])
        dict_data["temp"].append(data["main"]["temp"])
        dict_data["feels_like"].append(data["main"]["feels_like"])
        dict_data["humidity"].append(data["main"]["humidity"])
        dict_data["description"].append(data["weather"][0]["description"])
    df = pd.DataFrame(data=dict_data)
    df.to_csv(csv_path, index=False)


def load_csv(csv_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def analyse_csv(csv_path: Path) -> None:
    df = load_csv(csv_path=csv_path)
    hottest = df.nlargest(n=1, columns="temp")
    print(
        f"La ville la plus chaude est {hottest['name'].iloc[0]} avec une température de {hottest['temp'].iloc[0]}°C."
    )
    coldest = df.nsmallest(n=1, columns="temp")
    print(
        f"La ville la plus froide est {coldest['name'].iloc[0]} avec une température de {hottest['temp'].iloc[0]}°C."
    )
    mean_temp = df["temp"].mean()
    print(
        f"La température moyenne des villes est environ {round(float(mean_temp), 2)}°C."
    )


def main():
    villes = [
        "Paris",
        "Marseille",
        "Lyon",
        "Toulouse",
        "Nice",
        "Nantes",
        "Montpellier",
        "Strasbourg",
        "Bordeaux",
        "Lille",
    ]
    csv_path = DIR_PATH.joinpath("exo5.csv")
    # create_csv(csv_path=csv_path, villes=villes)

    analyse_csv(csv_path=csv_path)


if __name__ == "__main__":
    main()
