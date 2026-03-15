from app_v2_1.models import NamingPolicy, SensorEntity
from app_v2_1.normalizers.entity_naming_policy import EntityNamingPolicy


def test_keep_local_id() -> None:
    entity = SensorEntity(id="temp raw", name="Temp Raw", provider="mqtt", role="input", parent="zone_01", source={"topic": "a/b"})
    policy = EntityNamingPolicy(NamingPolicy(mode="keep_local_id", separator="_"))
    assert policy.exported_id_for(entity) == "temp_raw"


def test_prefix_parent() -> None:
    entity = SensorEntity(id="temp raw", name="Temp Raw", provider="mqtt", role="input", parent="zone 01", source={"topic": "a/b"})
    policy = EntityNamingPolicy(NamingPolicy(mode="prefix_parent", separator="_"))
    assert policy.exported_id_for(entity) == "zone_01_temp_raw"
