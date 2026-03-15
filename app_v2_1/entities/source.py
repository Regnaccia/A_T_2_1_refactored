from __future__ import annotations

from pydantic import Field

from app_v2_1.entities.strict import StrictModel


class MqttSource(StrictModel):
    topic: str = Field(min_length=1)


SourceConfig = MqttSource
