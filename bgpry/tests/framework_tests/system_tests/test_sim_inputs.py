from itertools import product

import pytest

from bgpry.simulation_engine import BGPSimplePolicy
from bgpry.simulation_engine import BGPPolicy
from bgpry.simulation_engine import ROVPolicy
from bgpry.simulation_engine import ROVSimplePolicy
from bgpry.simulation_engine import RealROVSimplePolicy
from bgpry.simulation_engine import RealPeerROVSimplePolicy

from bgpry.simulation_framework import NonRoutedPrefixHijack
from bgpry.simulation_framework import NonRoutedSuperprefixHijack
from bgpry.simulation_framework import NonRoutedSuperprefixPrefixHijack
from bgpry.simulation_framework import PrefixHijack
from bgpry.simulation_framework import ValidPrefix
from bgpry.simulation_framework import SubprefixHijack
from bgpry.simulation_framework import SuperprefixPrefixHijack
from bgpry.simulation_framework import ScenarioConfig

from bgpry.simulation_framework import Simulation

Policy_CLPolicySES = (
    BGPSimplePolicy,
    BGPPolicy,
    ROVPolicy,
    ROVSimplePolicy,
    RealROVSimplePolicy,
    RealPeerROVSimplePolicy,
)

SCENARIOS = (
    NonRoutedPrefixHijack,
    NonRoutedSuperprefixHijack,
    NonRoutedSuperprefixPrefixHijack,
    PrefixHijack,
    SubprefixHijack,
    SuperprefixPrefixHijack,
    ValidPrefix,
)
NUM_ATTACKERS = (1, 2)
PARSE_CPUS = (1, 2)


# Really does need all these combos
# Since certain as classes might break with mp
@pytest.mark.slow
@pytest.mark.framework
@pytest.mark.parametrize(
    "AdoptPolicyCls, BasePolicyCls, ScenarioCls, num_attackers, parse_cpus",
    [
        x
        for x in product(
            *[
                Policy_CLPolicySES,
                Policy_CLPolicySES,
                SCENARIOS,
                NUM_ATTACKERS,
                PARSE_CPUS,
            ]
        )
        # Where BasePolicyCls != AdoptPolicyCls
        if x[0] != x[1]
    ],
)
def test_sim_inputs(
    AdoptPolicyCls, BasePolicyCls, ScenarioCls, num_attackers, parse_cpus, tmp_path
):
    """Test basic functionality of process_incoming_anns"""

    sim = Simulation(
        percent_adoptions=(0.0, 0.5, 1.0),
        scenario_configs=(
            ScenarioConfig(
                ScenarioCls=ScenarioCls,
                AdoptPolicyCls=AdoptPolicyCls,
                BasePolicyCls=BasePolicyCls,
                num_attackers=num_attackers,
            ),
        ),
        num_trials=2,
        output_dir=tmp_path / "test_sim_inputs",
        parse_cpus=parse_cpus,
    )
    sim.run()
