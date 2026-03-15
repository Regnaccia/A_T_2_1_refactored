from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class YamlLoaderError(RuntimeError):
    pass


def read_yaml_file(path: Path) -> Any:
    if not path.exists():
        raise YamlLoaderError(f"YAML file not found: {path}")
    if not path.is_file():
        raise YamlLoaderError(f"YAML path is not a file: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise YamlLoaderError(f"Invalid YAML in file '{path}': {exc}") from exc
