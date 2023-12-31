from bgpry.caida_collector import CustomerProviderLink as CPLink


from .graph_info import GraphInfo
from bgpry.enums import ASNs


graph_046 = GraphInfo(
    peer_links=set([]),
    customer_provider_links=set(
        [
            CPLink(provider_asn=11, customer_asn=32),
            CPLink(provider_asn=11, customer_asn=77),
            CPLink(provider_asn=77, customer_asn=44),
            CPLink(provider_asn=44, customer_asn=33),
            CPLink(provider_asn=44, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=44, customer_asn=ASNs.VICTIM.value),
        ]
    ),
)
