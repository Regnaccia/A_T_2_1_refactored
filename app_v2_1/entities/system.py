from __future__ import annotations

from collections import Counter

from pydantic import Field, field_validator, model_validator

from app_v2_1.entities.strict import StrictModel


class MqttConfig(StrictModel):
    broker: str = Field(min_length=1)
    port: int = Field(ge=1, le=65535)
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class SystemConfig(StrictModel):
    system_name: str = Field(min_length=1)
    mqtt_config: str = Field(min_length=1)
    instances_package: str = Field(min_length=1)


class PackageConfig(StrictModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    type: str = Field(min_length=1)
    router: str = Field(min_length=1)
    initialize: bool = True

    @field_validator("type")
    @classmethod
    def normalize_type(cls, value: str) -> str:
        return value.lower()


class RouterConfig(StrictModel):
    entities: list[str] = Field(default_factory=list)


class SystemAssembly(StrictModel):
    name: str
    mqtt: MqttConfig
    instances: list[PackageConfig]

    @model_validator(mode="after")
    def validate_instance_package(self) -> "SystemAssembly":
        initialized = [item for item in self.instances if item.initialize]
        if not initialized:
            raise ValueError("No initialized instances found in instances package.")
        ids = [item.id for item in initialized]
        duplicate_ids = sorted([key for key, count in Counter(ids).items() if count > 1])
        if duplicate_ids:
            raise ValueError(f"Duplicate initialized instance ids detected: {duplicate_ids}")
        for required_type in ("system", "common"):
            matching = [item for item in initialized if item.type == required_type]
            if len(matching) == 0:
                raise ValueError(f"No initialized '{required_type}' instance found.")
            if len(matching) > 1:
                raise ValueError(f"More than one initialized '{required_type}' instance found.")
        return self
