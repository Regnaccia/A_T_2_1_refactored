from __future__ import annotations

from pathlib import Path


def resolve_config_path(base_path: Path, file_path: str) -> Path:
    normalized = file_path.replace("\\", "/")
    path = Path(normalized)
    if path.is_absolute():
        return path
    return (base_path / path).resolve()
