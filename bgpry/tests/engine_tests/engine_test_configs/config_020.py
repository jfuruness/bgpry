from frozendict import frozendict
from bgpry.tests.engine_tests.graphs import graph_017
from bgpry.tests.engine_tests.utils import EngineTestConfig

from bgpry.simulation_engine import BGPPolicy
from bgpry.enums import ASNs
from bgpry.simulation_framework import ScenarioConfig, ValidPrefix


config_020 = EngineTestConfig(
    name="020",
    desc="Test of relationship preference",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BasePolicyCls=BGPPolicy,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(),
    ),
    graph=graph_017,
)