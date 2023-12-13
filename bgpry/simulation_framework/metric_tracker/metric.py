from collections import defaultdict
from dataclasses import replace
from typing import Any, Optional, Type

from bgpry.enums import Plane, Outcomes
from bgpry.caida_collector import AS
from bgpry.simulation_engine import BGPSimplePolicy, SimulationEngine
from bgpry.simulation_framework.scenarios import Scenario

from .metric_key import MetricKey


class Metric:
    """Tracks a single metric"""

    def __init__(
        self,
        metric_key: MetricKey,
        as_classes_used: frozenset[Type[BGPSimplePolicy]],
        percents: Optional[defaultdict[MetricKey, list[float]]] = None,
    ) -> None:
        self.metric_key: MetricKey = metric_key
        self.as_classes_used: frozenset[Type[BGPSimplePolicy]] = as_classes_used
        self._numerators: dict[type[BGPSimplePolicy] | Any, float] = {
            k: 0 for k in as_classes_used
        }
        self._denominators: dict[type[BGPSimplePolicy] | Any, float] = {
            k: 0 for k in as_classes_used
        }
        # Used for aggregate statistics with any AS class
        self._numerators[Any] = 0
        self._denominators[Any] = 0
        if percents:
            self.percents: defaultdict[MetricKey, list[float]] = percents
        else:
            self.percents = defaultdict(list)

    def __add__(self, other):
        """Adds metric classes together"""

        if isinstance(other, Metric):
            agg_percents = defaultdict(list)
            for obj in (self, other):
                for metric_key, percent_list in obj.percents.items():
                    agg_percents[metric_key].extend(percent_list)
            return Metric(
                metric_key=self.metric_key,
                as_classes_used=self.as_classes_used,
                percents=agg_percents,
            )
        else:
            return NotImplemented

    def save_percents(self) -> None:
        """Returns percentages to be added to all metrics"""

        percents = defaultdict(list)
        for (PolicyCls, numerator), (DenomPolicyCls, denominator) in zip(
            self._numerators.items(), self._denominators.items()
        ):
            assert PolicyCls == DenomPolicyCls
            k = replace(self.metric_key, PolicyCls=PolicyCls)
            # Not pep8 but this case is way more common
            if not (numerator == 0 and denominator == 0):
                percents[k] = [100 * numerator / denominator]
            else:
                percents[k] = []
        self.percents = percents

    def add_data(
        self,
        *,
        as_obj: AS,
        engine: SimulationEngine,
        scenario: Scenario,
        ctrl_plane_outcome: Outcomes,
        data_plane_outcome: Outcomes,
    ):
        within_denom = self._add_denominator(
            as_obj=as_obj,
            engine=engine,
            scenario=scenario,
            ctrl_plane_outcome=ctrl_plane_outcome,
            data_plane_outcome=data_plane_outcome,
        )

        if within_denom:
            self._add_numerator(
                as_obj=as_obj,
                engine=engine,
                scenario=scenario,
                ctrl_plane_outcome=ctrl_plane_outcome,
                data_plane_outcome=data_plane_outcome,
            )

    def _add_numerator(
        self,
        *,
        as_obj: AS,
        engine: SimulationEngine,
        scenario: Scenario,
        ctrl_plane_outcome: Outcomes,
        data_plane_outcome: Outcomes,
    ) -> None:
        """Adds to numerator if it is within the as group and the outcome is correct"""

        if self.metric_key.plane == Plane.DATA:
            outcome = data_plane_outcome
        elif self.metric_key.plane == Plane.CTRL:
            outcome = ctrl_plane_outcome
        else:
            raise NotImplementedError

        asn_group = engine.asn_groups[self.metric_key.as_group.value]
        if as_obj.asn in asn_group and outcome == self.metric_key.outcome:
            self._numerators[as_obj.policy.__class__] += 1
            self._numerators[Any] += 1

    def _add_denominator(
        self,
        *,
        as_obj: AS,
        engine: SimulationEngine,
        scenario: Scenario,
        ctrl_plane_outcome: Outcomes,
        data_plane_outcome: Outcomes,
    ) -> bool:
        """Adds to the denominator if it is within the as group"""

        if as_obj.asn in engine.asn_groups[self.metric_key.as_group.value]:
            self._denominators[as_obj.policy.__class__] += 1
            self._denominators[Any] += 1
            return True
        else:
            return False
