from pathlib import Path

from src.config import load_config
from src.logger import setup_logger
from src.pipeline import ETLPipeline

DIR_PATH = Path(__file__).parent.resolve()


def main() -> None:
    log_dir = DIR_PATH / "logs"
    if not log_dir.exists():
        log_dir.mkdir()
    log_path = log_dir / "tp1.log"
    logger = setup_logger(name="tp1", log_file=log_path)

    config_path = DIR_PATH / "config" / "config.yaml"
    config = load_config(config_path=config_path)
    config["DIR_OUTPUT"] = DIR_PATH / config["DIR_OUTPUT"]

    pipeline = ETLPipeline(config=config, logger=logger)
    pipeline.run()


if __name__ == "__main__":
    main()
