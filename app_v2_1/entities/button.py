from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity


class ButtonEntity(BaseEntity):
    domain: Literal["button"] = "button"

    @model_validator(mode="after")
    def validate_button(self) -> "ButtonEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'button' cannot be derived in v1.")
        self._validate_primitive_vs_derived()
        return self
