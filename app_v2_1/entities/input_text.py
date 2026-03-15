from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity
from app_v2_1.entities.enums import TextMode


class InputTextEntity(BaseEntity):
    domain: Literal["input_text"] = "input_text"
    min: int = 0
    max: int = 100
    initial: str | None = None
    pattern: str | None = None
    mode: TextMode = "text"

    @model_validator(mode="after")
    def validate_input_text(self) -> "InputTextEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'input_text' cannot be derived in v1.")
        if self.min < 0:
            raise ValueError("InputText min cannot be negative.")
        if self.max < self.min:
            raise ValueError("InputText max cannot be lower than min.")
        if self.max > 255:
            raise ValueError("InputText max cannot exceed 255.")
        if self.initial is not None:
            if len(self.initial) < self.min:
                raise ValueError("InputText initial is shorter than min.")
            if len(self.initial) > self.max:
                raise ValueError("InputText initial is longer than max.")
        self._validate_primitive_vs_derived()
        return self
