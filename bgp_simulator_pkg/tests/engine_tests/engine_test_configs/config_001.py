from typing import Dict, Type

from caida_collector_pkg import AS

from ..graphs import Graph001
from ..utils import EngineTestConfig

from ....simulation_engine import BGPSimpleAS
from ....enums import ASNs
from ....simulation_framework import ScenarioConfig, SubprefixHijack


config_001 = EngineTestConfig(
    name="001"
    desc="BGP hidden hijack (with simple AS)"
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        override_attacker_asns={ASNs.ATTACKER.value},
        override_victim_asns={ASNs.VICTIM.value},
    )
    graph = Graph001()
)
