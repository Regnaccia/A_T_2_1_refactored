from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from app_v2_1.entities.enums import Provider, Role
from app_v2_1.entities.source import SourceConfig
from app_v2_1.entities.strict import StrictModel


class BaseEntity(StrictModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    parent: str = Field(min_length=1)

    provider: Provider
    role: Role

    expose: bool = True
    icon: str | None = None
    unit_of_measurement: str | None = None
    device_class: str | None = None
    entity_category: str | None = None
    enabled_by_default: bool = True

    source: SourceConfig | None = None
    dependencies: list[str] = Field(default_factory=list)
    evaluation: Any | None = None

    @field_validator("dependencies")
    @classmethod
    def validate_dependencies_not_blank(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value or not value.strip():
                raise ValueError("Dependencies cannot contain empty values.")
        return values

    @property
    def is_derived(self) -> bool:
        return self.provider == "derived"

    @property
    def full_id(self) -> str:
        return f"{self.parent}.{self.id}"

    def _validate_primitive_vs_derived(self) -> None:
        has_deps = len(self.dependencies) > 0
        has_eval = self.evaluation is not None
        has_source = self.source is not None

        if self.provider == "derived":
            if not has_deps:
                raise ValueError("Derived entity requires at least one dependency.")
            if not has_eval:
                raise ValueError("Derived entity requires an evaluation block.")
            if has_source:
                raise ValueError("Derived entity cannot define source.")
        else:
            if has_deps:
                raise ValueError("Primitive entity cannot define dependencies.")
            if has_eval:
                raise ValueError("Primitive entity cannot define evaluation.")

        if self.provider == "mqtt" and self.source is None:
            raise ValueError("MQTT entity requires source.topic.")
        if self.provider != "mqtt" and has_source:
            raise ValueError("Source is currently supported only for provider='mqtt'.")
