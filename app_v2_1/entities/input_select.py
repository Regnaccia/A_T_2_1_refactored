from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from app_v2_1.entities.base import BaseEntity


class InputSelectEntity(BaseEntity):
    domain: Literal["input_select"] = "input_select"
    options: list[str] = Field(default_factory=list)
    initial: str | None = None

    @model_validator(mode="after")
    def validate_input_select(self) -> "InputSelectEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'input_select' cannot be derived in v1.")
        if not self.options:
            raise ValueError("InputSelect requires at least one option.")
        if self.initial is not None and self.initial not in self.options:
            raise ValueError("InputSelect initial must be included in options.")
        self._validate_primitive_vs_derived()
        return self
