from __future__ import annotations
from typing import TYPE_CHECKING

from bgpry.simulation_framework.scenarios.scenario import Scenario
from bgpry.enums import Prefixes
from bgpry.enums import Relationships
from bgpry.enums import Timestamps


if TYPE_CHECKING:
    from bgpry.simulation_engine import Announcement


class NonRoutedPrefixHijack(Scenario):
    """Non routed prefix hijack (ROA of AS 0)"""

    def _get_announcements(self, *args, **kwargs) -> tuple["Announcement", ...]:
        """Returns non routed prefix announcement from attacker

        for subclasses of this EngineInput, you can set AnnCls equal to
        something other than Announcement
        """

        anns = list()
        for attacker_asn in self.attacker_asns:
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.PREFIX.value,
                    as_path=(attacker_asn,),
                    timestamp=Timestamps.ATTACKER.value,
                    seed_asn=attacker_asn,
                    roa_valid_length=True,
                    roa_origin=0,
                    recv_relationship=Relationships.ORIGIN,
                )
            )
        return tuple(anns)
