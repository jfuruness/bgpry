from frozendict import frozendict
from bgpry.tests.engine_tests.graphs import graph_003
from bgpry.tests.engine_tests.utils import EngineTestConfig

from bgpry.simulation_engine import ROVSimplePolicy, BGPSimplePolicy
from bgpry.enums import ASNs
from bgpry.simulation_framework import ScenarioConfig, SubprefixHijack


config_007 = EngineTestConfig(
    name="007",
    desc="Fig 2 (ROVSimplePolicy)",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BasePolicyCls=BGPSimplePolicy,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        AdoptPolicyCls=ROVSimplePolicy,
        override_non_default_asn_cls_dict=frozendict(
            {3: ROVSimplePolicy, 4: ROVSimplePolicy}
        ),
    ),
    graph=graph_003,
)
