from typing import TYPE_CHECKING

from bgpry.simulation_framework.scenarios.scenario import Scenario
from bgpry.enums import Prefixes
from bgpry.enums import Relationships
from bgpry.enums import Timestamps


if TYPE_CHECKING:
    from bgpry.simulation_engine import Announcement


class SuperprefixPrefixHijack(Scenario):
    """Superprefix prefix attack

    This is an attack where the attacker
    announces a prefix hijack (invalid by roa origin)
    and also announces a superprefix of the prefix (ROA unknown)
    and the victim announces their own prefix
    """

    def _get_announcements(self, *args, **kwargs) -> tuple["Announcement", ...]:
        """Returns victim+attacker prefix ann, attacker superprefix ann

        for subclasses of this EngineInput, you can set AnnCls equal to
        something other than Announcement
        """

        anns = list()
        for victim_asn in self.victim_asns:
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.PREFIX.value,
                    as_path=(victim_asn,),
                    timestamp=Timestamps.VICTIM.value,
                    seed_asn=victim_asn,
                    roa_valid_length=True,
                    roa_origin=victim_asn,
                    recv_relationship=Relationships.ORIGIN,
                )
            )

        err: str = "Fix the roa_origins of the " "announcements for multiple victims"
        assert len(self.victim_asns) == 1, err

        roa_origin: int = next(iter(self.victim_asns))

        for attacker_asn in self.attacker_asns:
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.PREFIX.value,
                    as_path=(attacker_asn,),
                    timestamp=Timestamps.ATTACKER.value,
                    seed_asn=attacker_asn,
                    roa_valid_length=True,
                    roa_origin=roa_origin,
                    recv_relationship=Relationships.ORIGIN,
                )
            )
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.SUPERPREFIX.value,
                    as_path=(attacker_asn,),
                    timestamp=Timestamps.ATTACKER.value,
                    seed_asn=attacker_asn,
                    roa_valid_length=None,
                    roa_origin=None,
                    recv_relationship=Relationships.ORIGIN,
                )
            )

        return tuple(anns)
