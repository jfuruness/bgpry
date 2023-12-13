from frozendict import frozendict
from bgpry.tests.engine_tests.graphs import graph_018
from bgpry.tests.engine_tests.utils import EngineTestConfig

from bgpry.simulation_engine import ROVPolicy
from bgpry.enums import ASNs
from bgpry.simulation_framework import ScenarioConfig, ValidPrefix


config_018 = EngineTestConfig(
    name="018",
    desc="Test of path length preference",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BasePolicyCls=ROVPolicy,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(),
    ),
    graph=graph_018,
)
