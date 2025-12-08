from pathlib import Path

from yaml import safe_load


def load_config(file_path: Path):
    """Lit le fichier config/config.yaml et renvoie un dict."""
    with open(file_path, "r", encoding="utf-8") as f:
        config = safe_load(f)
    return config
