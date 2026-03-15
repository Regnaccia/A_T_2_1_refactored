from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity


class InputBooleanEntity(BaseEntity):
    domain: Literal["input_boolean"] = "input_boolean"
    initial: bool | None = None

    @model_validator(mode="after")
    def validate_input_boolean(self) -> "InputBooleanEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'input_boolean' cannot be derived in v1.")
        self._validate_primitive_vs_derived()
        return self
