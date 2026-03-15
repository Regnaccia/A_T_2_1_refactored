from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity
from app_v2_1.entities.enums import NumberMode


class InputNumberEntity(BaseEntity):
    domain: Literal["input_number"] = "input_number"
    min: float
    max: float
    step: float = 1.0
    initial: float | None = None
    mode: NumberMode = "slider"

    @model_validator(mode="after")
    def validate_input_number(self) -> "InputNumberEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'input_number' cannot be derived in v1.")
        if self.min > self.max:
            raise ValueError("InputNumber min cannot be greater than max.")
        if self.step <= 0:
            raise ValueError("InputNumber step must be > 0.")
        if self.initial is not None and not (self.min <= self.initial <= self.max):
            raise ValueError("InputNumber initial must be within [min, max].")
        self._validate_primitive_vs_derived()
        return self
