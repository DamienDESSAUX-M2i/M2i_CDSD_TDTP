from pathlib import Path
from typing import Any

from yaml import safe_load


def load_config(config_path: Path) -> dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as f:
        return safe_load(f)
