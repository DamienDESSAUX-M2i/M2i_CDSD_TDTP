import os
import yaml

from src.utils.logger import setup_logger
from src.pipeline_api_demo import ApiDemoPipeline


def load_config():
    """Lit le fichier config/config.yaml et renvoie un dict."""
    config_path = os.path.join("config", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def main():
    # 1) Logger principal
    logger = setup_logger("ETL_API", "logs/etl_api.log")

    # 2) Chargement de la configuration
    config = load_config()

    # 3) Instanciation de la pipeline API
    pipeline = ApiDemoPipeline(config=config, logger=logger)

    # 4) Exécution du pipeline
    pipeline.run()


if __name__ == "__main__":
    main()