from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity
from app_v2_1.entities.enums import NumberMode


class NumberEntity(BaseEntity):
    domain: Literal["number"] = "number"
    min: float | None = None
    max: float | None = None
    step: float = 1.0
    mode: NumberMode = "slider"

    @model_validator(mode="after")
    def validate_number(self) -> "NumberEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'number' cannot be derived in v1.")
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("Number min cannot be greater than max.")
        if self.step <= 0:
            raise ValueError("Number step must be > 0.")
        self._validate_primitive_vs_derived()
        return self
