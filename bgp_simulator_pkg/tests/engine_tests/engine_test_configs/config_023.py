from typing import Dict, Type

from caida_collector_pkg import AS

from ..graphs import Graph019
from ..utils import EngineTestConfig

from ....simulation_engine import BGPSimpleAS
from ....enums import ASNs
from ....simulation_framework import ScenarioConfig, ValidPrefix


config_023 = EngineTestConfig(
    name="023",
    desc="Test of tiebreak preference",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BaseASCls=BGPSimpleAS,
        override_attacker_asns={ASNs.ATTACKER.value},
        override_victim_asns={ASNs.VICTIM.value},
    ),
    graph=Graph019(),
)
