from pathlib import Path
import time

from bgpry.simulation_engine import ROVSimplePolicy
from bgpry.enums import SpecialPercentAdoptions
from bgpry.simulation_framework import Simulation, SubprefixHijack, ScenarioConfig


class NoopGraphFactory:
    def __init__(*args, **kwargs):
        pass
    """Writes no graphs, which we don't care about for time trials of engine"""
    def generate_graphs(*args, **kwargs):
        pass


def main():
    """Runs the benchmark"""

    sim = Simulation(
        python_hash_seed=0,
        percent_adoptions=(
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.5,
            0.8,
            SpecialPercentAdoptions.ALL_BUT_ONE,
        ),
        scenario_configs=(
            ScenarioConfig(ScenarioCls=SubprefixHijack, AdoptPolicyCls=ROVSimplePolicy),
        ),
        output_dir=Path("~/Desktop/main_ex").expanduser(),
        num_trials=1,
        parse_cpus=1,
    )
    sim.run(GraphFactoryCls=NoopGraphFactory)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(time.perf_counter() - start)
