from __future__ import annotations

from pathlib import Path
from typing import Any

from app_v2_1.loaders.yaml_loader import read_yaml_file
from app_v2_1.utils.logging import LogMode, indent, log
from app_v2_1.utils.paths import resolve_config_path


def load_yaml_config(
    *,
    base_path: Path,
    file_path: str,
    log_mode: LogMode,
    label: str,
    level: int,
) -> Any:
    resolved_path = resolve_config_path(base_path, file_path)
    log(log_mode, indent(f" Loading {label}: {resolved_path}", level), level=level)
    data = read_yaml_file(resolved_path)
    if data is None:
        raise ValueError(f"{label} is empty: {resolved_path}")
    return data
