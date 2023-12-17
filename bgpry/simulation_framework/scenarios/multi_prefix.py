from typing import TYPE_CHECKING

from .scenario import Scenario
# from bgpry.enums import Prefixes
from bgpry.enums import Relationships
from bgpry.enums import Timestamps


if TYPE_CHECKING:
    from bgpry.simulation_engine import Announcement


def generate_cidr_prefixes(start_ip, subnet_mask, count=1000):
    prefixes = []
    # Split the start IP into octets
    octets = [int(octet) for octet in start_ip.split('.')]

    for _ in range(count):
        # Increment the third octet after the fourth octet hits 255
        if octets[3] == 255:
            octets[3] = 0
            octets[2] += 1
            # Increment the second octet after the third octet hits 255
            if octets[2] == 255:
                octets[2] = 0
                octets[1] += 1
                # Increment the first octet after the second octet hits 255
                if octets[1] == 255:
                    octets[1] = 0
                    octets[0] += 1

        # Format the current IP address
        current_ip = '.'.join(map(str, octets))
        # Combine IP with subnet mask
        cidr = f"{current_ip}/{subnet_mask}"
        prefixes.append(cidr)

        # Increment the fourth octet
        octets[3] += 1

    return prefixes

# Example usage
cidr_prefixes = generate_cidr_prefixes('1.0.0.0', 32)

class MultiPrefix(Scenario):
    """A valid prefix engine input, mainly for testing"""

    def _get_announcements(self, engine, prev_scenario) -> tuple["Announcement", ...]:
        """Returns a valid prefix announcement

        for subclasses of this EngineInput, you can set AnnCls equal to
        something other than Announcement
        """

        anns = list()
        with open("/home/anon/mrt_data/2023-12-12_00:00:00/formatted/non_urlhttp%3A__archive.routeviews.org_route-views.bknix_bgpdata_2023.12_RIBS_rib.20231212.0000.bz2/1000/12.tsv") as f:
            import csv
            from tqdm import tqdm
            reader = csv.DictReader(f, delimiter="\t")
            for i, row in enumerate(tqdm(reader, desc="Reading anns", total=100)):
                if i > 100:
                    continue
                as_path = row["as_path"]
                if "{" in as_path:
                    continue
                else:
                    as_path = tuple([int(x) for x in row["as_path"].split(" ")])

                if as_path[-1] not in engine.as_dict:
                    # Since we removed stubs, if we see a stub ann, just seed 1 above it
                    if len(as_path) >= 2 and as_path[-2] in engine.as_dict:
                        as_path = as_path[:-1]
                    else:
                        continue
                anns.append(
                    self.scenario_config.AnnCls(
                        prefix=row["prefix"],
                        as_path=tuple([as_path[-1]]),
                        timestamp=int(row["timestamp"]),
                        seed_asn=as_path[-1],
                        roa_valid_length=True,
                        roa_origin=as_path[-1],
                        recv_relationship=Relationships.ORIGIN,
                    )
                )
        print(f"Total anns {len(anns)}")
        return tuple(anns)

    def _get_attacker_asns(self, *args, **kwargs):
        return set()
