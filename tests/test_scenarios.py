import asyncio

from scenarios import SCENARIOS, list_scenarios
from scenarios.base import INTENSITY_COUNTS


class _FakeFarm:
    def __init__(self):
        self.spawned = []

    async def spawn_charger(self, cp_id, profile_name=None, ocpp_version=None, quirks=None, **kw):
        self.spawned.append((cp_id, profile_name, ocpp_version))
        return object()


def test_registry_has_17_scenarios():
    assert len(SCENARIOS) == 17
    assert len(list_scenarios()) == 17


def test_all_scenarios_instantiate_at_all_intensities():
    for name, cls in SCENARIOS.items():
        for intensity in INTENSITY_COUNTS:
            assert cls(_FakeFarm(), intensity).name == name


def test_spawn_forwards_ocpp_version_and_profile():
    farm = _FakeFarm()
    sc = next(iter(SCENARIOS.values()))(farm, "low", ocpp_version="2.0.1")
    asyncio.run(sc._spawn_charger("X-1"))
    assert farm.spawned == [("X-1", "ENC-DCL120B", "2.0.1")]
    sc = next(iter(SCENARIOS.values()))(farm, "low")
    asyncio.run(sc._spawn_charger("X-2"))
    assert farm.spawned[-1] == ("X-2", "ENC-DCL120B-16", "1.6")
