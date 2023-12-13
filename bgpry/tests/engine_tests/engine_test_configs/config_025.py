from frozendict import frozendict
from bgpry.tests.engine_tests.graphs import graph_019
from bgpry.tests.engine_tests.utils import EngineTestConfig

from bgpry.simulation_engine import ROVSimplePolicy
from bgpry.enums import ASNs
from bgpry.simulation_framework import ScenarioConfig, ValidPrefix


config_025 = EngineTestConfig(
    name="025",
    desc="Test of tiebreak preference",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BasePolicyCls=ROVSimplePolicy,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(),
    ),
    graph=graph_019,
)
