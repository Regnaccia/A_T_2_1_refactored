from __future__ import annotations

import re


def slugify(value: str, separator: str = "_") -> str:
    normalized = value.strip().lower().replace("-", separator).replace(" ", separator)
    normalized = re.sub(rf"[^a-z0-9{re.escape(separator)}]", separator, normalized)
    normalized = re.sub(rf"{re.escape(separator)}+", separator, normalized)
    return normalized.strip(separator)
