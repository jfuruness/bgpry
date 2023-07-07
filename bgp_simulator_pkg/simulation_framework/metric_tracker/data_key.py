from dataclasses import dataclass
from typing import Union

from .metric import Metric

from bgp_simulator_pkg.enums import SpecialPercentAdoptions


@dataclass(frozen=True)
class DataKey:
    """Key for storing data within the MetricTracker"""

    propagation_round: int
    percent_adopt: Union[float, SpecialPercentAdoptions]
    scenario_label: str
    MetricCls: type[Metric]