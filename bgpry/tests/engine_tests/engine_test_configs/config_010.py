from frozendict import frozendict
from bgpry.tests.engine_tests.graphs import graph_003
from bgpry.tests.engine_tests.utils import EngineTestConfig

from bgpry.simulation_engine import BGPSimplePolicy
from bgpry.enums import ASNs
from bgpry.simulation_framework import ScenarioConfig, SubprefixHijack


config_010 = EngineTestConfig(
    name="010",
    desc="Fig 2 (ROVSimplePolicy)",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BasePolicyCls=BGPSimplePolicy,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(),
    ),
    graph=graph_003,
)
