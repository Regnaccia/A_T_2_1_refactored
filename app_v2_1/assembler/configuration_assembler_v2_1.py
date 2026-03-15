from __future__ import annotations

from pathlib import Path

from app_v2_1.assembler.instance_assembler_v2_1 import InstanceAssemblerV2_1
from app_v2_1.assembler.system_assembler_v2_1 import SystemAssemblerV2_1
from app_v2_1.models import (
    AssembledConfiguration,
    BuiltEntity,
    BuiltInstance,
    BuiltInstanceInfo,
    BuiltSystemInfo,
    NamingPolicy,
)
from app_v2_1.normalizers.entity_naming_policy import EntityNamingPolicy
from app_v2_1.utils.logging import indent, log


class ConfigurationAssemblerV2_1:
    def __init__(
        self,
        *,
        base_path: Path,
        system_file: str,
        naming_policy: NamingPolicy | None = None,
        log_mode=None,
    ) -> None:
        self.base_path = Path(base_path)
        self.system_file = system_file
        self.naming_policy = naming_policy or NamingPolicy()
        self.log_mode = log_mode

    def assemble(self) -> AssembledConfiguration:
        log(self.log_mode, indent("⚙️ Assembling configuration v2.1", 0), level=0)

        system = SystemAssemblerV2_1(
            base_path=self.base_path,
            system_file=self.system_file,
            log_mode=self.log_mode,
        ).assemble()

        initialized_instances = [instance for instance in system.instances if instance.initialize]
        instance_assemblies = [
            InstanceAssemblerV2_1(
                base_path=self.base_path,
                instance=instance,
                log_mode=self.log_mode,
            ).assemble()
            for instance in initialized_instances
        ]

        naming = EntityNamingPolicy(self.naming_policy)
        built_entities: list[BuiltEntity] = []
        built_instances: list[BuiltInstance] = []

        for instance in instance_assemblies:
            instance_exported_ids: list[str] = []
            for entity in instance.entities.iter_entities():
                exported_id = naming.exported_id_for(entity)
                built_entities.append(
                    BuiltEntity(
                        id=entity.id,
                        full_id=entity.full_id,
                        exported_id=exported_id,
                        name=entity.name,
                        parent=entity.parent,
                        domain=entity.domain,
                        provider=entity.provider,
                        role=entity.role,
                        expose=entity.expose,
                        source=entity.source,
                        dependencies=list(entity.dependencies),
                        evaluation=entity.evaluation.model_dump(mode="json") if entity.evaluation else None,
                    )
                )
                instance_exported_ids.append(exported_id)

            built_instances.append(
                BuiltInstance(
                    id=instance.id,
                    name=instance.name,
                    type=instance.type,
                    info=BuiltInstanceInfo(
                        router=instance.router_path,
                        entities=instance_exported_ids,
                        entities_count=len(instance_exported_ids),
                    ),
                )
            )

        return AssembledConfiguration(
            system=BuiltSystemInfo(
                name=system.name,
                instances=[instance.id for instance in instance_assemblies],
                instances_count=len(instance_assemblies),
            ),
            mqtt=system.mqtt,
            instances=built_instances,
            entities=built_entities,
            naming_policy=self.naming_policy,
        )
