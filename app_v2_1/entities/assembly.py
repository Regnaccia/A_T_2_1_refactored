from __future__ import annotations

from pydantic import computed_field, model_validator

from app_v2_1.entities.enums import Domain, NamingMode, Provider, Role
from app_v2_1.entities.manifest import InstanceEntityManifest
from app_v2_1.entities.source import SourceConfig
from app_v2_1.entities.strict import StrictModel
from app_v2_1.entities.system import MqttConfig, RouterConfig


class NamingPolicy(StrictModel):
    mode: NamingMode = "keep_local_id"
    separator: str = "_"


class InstanceAssembly(StrictModel):
    id: str
    name: str
    type: str
    router_path: str
    router: RouterConfig
    entities: InstanceEntityManifest

    @computed_field
    @property
    def initialized_entity_ids(self) -> list[str]:
        return [entity.id for entity in self.entities.iter_entities()]

    @computed_field
    @property
    def initialized_entity_count(self) -> int:
        return len(self.initialized_entity_ids)


class BuiltSystemInfo(StrictModel):
    name: str
    instances: list[str]
    instances_count: int


class BuiltInstanceInfo(StrictModel):
    router: str
    entities: list[str]
    entities_count: int


class BuiltInstance(StrictModel):
    id: str
    name: str
    type: str
    info: BuiltInstanceInfo


class BuiltEntity(StrictModel):
    id: str
    full_id: str
    exported_id: str
    name: str
    parent: str
    domain: Domain
    provider: Provider
    role: Role
    expose: bool
    source: SourceConfig | None = None
    dependencies: list[str]
    evaluation: dict | None = None


class AssembledConfiguration(StrictModel):
    system: BuiltSystemInfo
    mqtt: MqttConfig
    instances: list[BuiltInstance]
    entities: list[BuiltEntity]
    naming_policy: NamingPolicy

    @model_validator(mode="after")
    def validate_global_uniqueness(self) -> "AssembledConfiguration":
        full_ids = [entity.full_id for entity in self.entities]
        duplicate_full_ids = sorted({item for item in full_ids if full_ids.count(item) > 1})
        if duplicate_full_ids:
            raise ValueError(f"Duplicate exported entity ids detected: {duplicate_full_ids}")
        return self
