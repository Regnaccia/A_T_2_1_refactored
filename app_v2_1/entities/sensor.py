from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from app_v2_1.entities.base import BaseEntity
from app_v2_1.entities.evaluation import EvalMath, SensorEvaluation


class SensorEntity(BaseEntity):
    domain: Literal["sensor"] = "sensor"
    evaluation: SensorEvaluation | None = None

    @model_validator(mode="after")
    def validate_sensor(self) -> "SensorEntity":
        self._validate_primitive_vs_derived()

        if self.provider == "derived":
            assert self.evaluation is not None
            kind = self.evaluation.kind
            deps_count = len(self.dependencies)

            if kind == "copy" and deps_count != 1:
                raise ValueError("Sensor evaluation 'copy' requires exactly 1 dependency.")
            if kind == "map" and deps_count != 1:
                raise ValueError("Sensor evaluation 'map' requires exactly 1 dependency.")
            if kind == "math":
                assert isinstance(self.evaluation, EvalMath)
                op = self.evaluation.operator
                if op in {"add", "sub", "mul", "div"} and deps_count < 2:
                    raise ValueError(f"Sensor math '{op}' requires at least 2 dependencies.")
                if op in {"min", "max", "avg"} and deps_count < 1:
                    raise ValueError(f"Sensor math '{op}' requires at least 1 dependency.")
        return self
