from pathlib import Path

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from .graph_info import GraphInfo
from ....enums import ASNs


class G002(GraphInfo):
    r"""
    Test propagating up without multihomed support in the following test graph.
    Horizontal lines are peer relationships, vertical lines are customer-provider.

      1
      |
      2---3
     /|    \
    4 777-5 6

    Starting propagation at 5, all ASes should see the announcement.
    """

    def __init__(self):
        super(G002, self).__init__(
            peer_links=set([PeerLink(2, 3),
                            PeerLink(ASNs.VICTIM.value, 5)]),
            customer_provider_links=set(
                [CPLink(provider_asn=1, customer_asn=2),
                 CPLink(provider_asn=2, customer_asn=4),
                 CPLink(provider_asn=2, customer_asn=ASNs.VICTIM.value),
                 CPLink(provider_asn=3, customer_asn=6)]))
