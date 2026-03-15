from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity
from app_v2_1.entities.evaluation import BinarySensorEvaluation


class BinarySensorEntity(BaseEntity):
    domain: Literal["binary_sensor"] = "binary_sensor"
    evaluation: BinarySensorEvaluation | None = None

    @model_validator(mode="after")
    def validate_binary_sensor(self) -> "BinarySensorEntity":
        self._validate_primitive_vs_derived()

        if self.provider == "derived":
            assert self.evaluation is not None
            kind = self.evaluation.kind
            deps_count = len(self.dependencies)

            if kind in {"all_true", "any_true"} and deps_count < 1:
                raise ValueError(f"Binary sensor evaluation '{kind}' requires at least 1 dependency.")
            if kind == "not" and deps_count != 1:
                raise ValueError("Binary sensor evaluation 'not' requires exactly 1 dependency.")
            if kind == "equals" and deps_count != 1:
                raise ValueError("Binary sensor evaluation 'equals' requires exactly 1 dependency.")
            if kind == "threshold" and deps_count != 1:
                raise ValueError("Binary sensor evaluation 'threshold' requires exactly 1 dependency.")
        return self
