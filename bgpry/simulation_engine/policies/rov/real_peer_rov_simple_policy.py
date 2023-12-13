from bgpry.simulation_engine.policies.bgp import BGPSimplePolicy
from bgpry.simulation_engine.announcement import Announcement as Ann
from bgpry.enums import Relationships


class RealPeerROVSimplePolicy(BGPSimplePolicy):
    """An Policy that deploys ROV in real life, but only filters peers"""

    name: str = "RealPeerROVSimple"

    # mypy doesn't understand that this func is valid
    def _valid_ann(self, ann: Ann, *args, **kwargs) -> bool:  # type: ignore
        """Returns announcement validity

        Returns false if invalid by roa,
        otherwise uses standard BGP (such as no loops, etc)
        to determine validity

        Note that since this is real world ROV for peers, it only filters anns coming
        from peers
        """

        # Invalid by ROA is not valid by ROV
        # Since this type of real world ROV only does peer filtering, only peers here
        if ann.invalid_by_roa and ann.recv_relationship == Relationships.PEERS:
            return False
        # Use standard BGP to determine if the announcement is valid
        else:
            # Mypy doesn't map superclasses properly
            return super(RealPeerROVSimplePolicy, self)._valid_ann(  # type: ignore
                ann, *args, **kwargs
            )
