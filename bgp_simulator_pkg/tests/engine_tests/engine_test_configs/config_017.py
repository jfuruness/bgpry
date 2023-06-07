from typing import Dict, Type

from caida_collector_pkg import AS

from ..graphs import Graph018
from ..utils import EngineTestConfig

from ....simulation_engine import ROVSimpleAS
from ....enums import ASNs
from ....simulation_framework import ScenarioConfig, ValidPrefix


config_017 = EngineTestConfig(
    name="017",
    desc="Test of path length preference",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BaseASCls=ROVSimpleAS,
        override_attacker_asns={ASNs.ATTACKER.value},
        override_victim_asns={ASNs.VICTIM.value},
    ),
    graph=Graph018(),
)
