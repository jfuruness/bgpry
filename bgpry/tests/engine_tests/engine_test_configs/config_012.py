from frozendict import frozendict
from bgpry.tests.engine_tests.graphs import graph_006
from bgpry.tests.engine_tests.utils import EngineTestConfig

from bgpry.simulation_engine import BGPSimplePolicy, ROVPolicy
from bgpry.enums import ASNs
from bgpry.simulation_framework import ScenarioConfig, NonRoutedPrefixHijack


config_012 = EngineTestConfig(
    name="012",
    desc="NonRouted Prefix Hijack",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedPrefixHijack,
        AdoptPolicyCls=ROVPolicy,
        BasePolicyCls=BGPSimplePolicy,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({2: ROVPolicy}),
    ),
    graph=graph_006,
)
