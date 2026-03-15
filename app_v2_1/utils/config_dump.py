from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

import yaml

from app_v2_1.models import AssembledConfiguration

DumpFormat = Literal["json", "yaml"]


def config_dump_payload(config: AssembledConfiguration, fmt: DumpFormat = "json") -> str:
    payload = config.model_dump(mode="json")
    if fmt == "json":
        return json.dumps(payload, indent=2, ensure_ascii=False)
    if fmt == "yaml":
        return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)
    raise ValueError(f"Unsupported dump format: {fmt}")


def write_config_dump(config: AssembledConfiguration, output_path: Path, fmt: DumpFormat = "json") -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(config_dump_payload(config, fmt=fmt), encoding="utf-8")
    return output_path
