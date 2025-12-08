from pathlib import Path
from typing import Any

from yaml import safe_load


def load_config(file_path: Path) -> dict[str, Any]:
    """Load config.yaml file."""

    with open(file_path, "r", encoding="utf-8") as f:
        config = safe_load(f)
    return config
