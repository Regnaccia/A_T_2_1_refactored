from __future__ import annotations

from typing import Union

from pydantic import Field, model_validator

from app_v2_1.entities.enums import MathOperator, ThresholdOperator
from app_v2_1.entities.strict import StrictModel

ScalarValue = str | int | float | bool


class EvalAllTrue(StrictModel):
    kind: str = Field(default="all_true", frozen=True)


class EvalAnyTrue(StrictModel):
    kind: str = Field(default="any_true", frozen=True)


class EvalNot(StrictModel):
    kind: str = Field(default="not", frozen=True)


class EvalEquals(StrictModel):
    kind: str = Field(default="equals", frozen=True)
    target: ScalarValue


class EvalThreshold(StrictModel):
    kind: str = Field(default="threshold", frozen=True)
    operator: ThresholdOperator
    target: float


class EvalCopy(StrictModel):
    kind: str = Field(default="copy", frozen=True)


class EvalMath(StrictModel):
    kind: str = Field(default="math", frozen=True)
    operator: MathOperator


class EvalMap(StrictModel):
    kind: str = Field(default="map", frozen=True)
    mapping: dict[str, ScalarValue]

    @model_validator(mode="after")
    def validate_mapping_not_empty(self) -> "EvalMap":
        if not self.mapping:
            raise ValueError("Map evaluation requires at least one mapping entry.")
        return self


BinarySensorEvaluation = Union[
    EvalAllTrue,
    EvalAnyTrue,
    EvalNot,
    EvalEquals,
    EvalThreshold,
]

SensorEvaluation = Union[
    EvalCopy,
    EvalMath,
    EvalMap,
]
