from frozendict import frozendict
from bgpry.tests.engine_tests.graphs import graph_002
from bgpry.tests.engine_tests.utils import EngineTestConfig

from bgpry.simulation_engine import BGPPolicy
from bgpry.enums import ASNs
from bgpry.simulation_framework import ScenarioConfig, ValidPrefix


config_004 = EngineTestConfig(
    name="004",
    desc="Basic BGP Propagation (with full BGP AS)",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BasePolicyCls=BGPPolicy,
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(),
    ),
    graph=graph_002,
)
