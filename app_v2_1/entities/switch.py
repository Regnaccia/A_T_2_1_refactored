from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity


class SwitchEntity(BaseEntity):
    domain: Literal["switch"] = "switch"

    @model_validator(mode="after")
    def validate_switch(self) -> "SwitchEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'switch' cannot be derived in v1.")
        self._validate_primitive_vs_derived()
        return self
