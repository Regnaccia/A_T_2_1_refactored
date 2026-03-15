from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity


class InputButtonEntity(BaseEntity):
    domain: Literal["input_button"] = "input_button"

    @model_validator(mode="after")
    def validate_input_button(self) -> "InputButtonEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'input_button' cannot be derived in v1.")
        self._validate_primitive_vs_derived()
        return self
