from dataclasses import dataclass
from typing import Any, Optional, Union

from bgpry.enums import ASGroups, Plane, Outcomes
from bgpry.simulation_engine import BGPSimplePolicy


@dataclass(frozen=True, slots=True)
class MetricKey:
    """Key for storing data within each metric"""

    plane: Plane
    as_group: ASGroups
    outcome: Outcomes
    PolicyCls: Union[Optional[type[BGPSimplePolicy]], Any] = None
