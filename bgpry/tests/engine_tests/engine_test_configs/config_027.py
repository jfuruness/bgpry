from frozendict import frozendict
from bgpry.tests.engine_tests.graphs import graph_040
from bgpry.tests.engine_tests.utils import EngineTestConfig

from bgpry.simulation_engine import BGPSimplePolicy
from bgpry.simulation_framework import ScenarioConfig, ValidPrefix


config_027 = EngineTestConfig(
    name="027",
    desc="Test of customer preference",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BasePolicyCls=BGPSimplePolicy,
        num_victims=3,
        override_victim_asns=frozenset({2, 3, 4}),
        override_non_default_asn_cls_dict=frozendict(),
    ),
    graph=graph_040,
)
