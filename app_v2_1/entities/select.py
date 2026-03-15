from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from app_v2_1.entities.base import BaseEntity


class SelectEntity(BaseEntity):
    domain: Literal["select"] = "select"
    options: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_select(self) -> "SelectEntity":
        if self.provider == "derived":
            raise ValueError("Domain 'select' cannot be derived in v1.")
        if not self.options:
            raise ValueError("Select entity requires at least one option.")
        self._validate_primitive_vs_derived()
        return self
