from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity
from app_v2_1.entities.enums import TextMode


class TextEntity(BaseEntity):
    domain: Literal["text"] = "text"
    min: int = 0
    max: int = 100
    pattern: str | None = None
    mode: TextMode = "text"

    @model_validator(mode="after")
    def validate_text(self) -> "TextEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'text' cannot be derived in v1.")
        if self.min < 0:
            raise ValueError("Text min cannot be negative.")
        if self.max < self.min:
            raise ValueError("Text max cannot be lower than min.")
        if self.max > 255:
            raise ValueError("Text max cannot exceed 255.")
        self._validate_primitive_vs_derived()
        return self
