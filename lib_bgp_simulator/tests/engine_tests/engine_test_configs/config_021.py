from ..graphs import Graph017
from ..utils import EngineTestConfig

from ....engine import ROVSimpleAS
from ....enums import ASNs
from ....scenarios import ValidPrefix


class Config021(EngineTestConfig):
    """Contains config options to run a test"""

    name = "021"
    desc = "Test of relationship preference"
    scenario = ValidPrefix(attacker_asn=ASNs.ATTACKER.value,
                           victim_asn=ASNs.VICTIM.value,
                           AdoptASCls=None,
                           BaseASCls=ROVSimpleAS)
    graph = Graph017()
    non_default_as_cls_dict = dict()
    propagation_rounds = 1