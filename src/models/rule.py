from pydantic import BaseModel, constr
from ipaddress import IPv4Network, IPv6Network


class Rule(BaseModel):
    id: str
    policy_id: str
    name: constr(min_length=0)
    ip_proto: IPv4Network or IPv6Network
    source_port: int

    def to_dict(self):
        return {
            "id": self.id,
            "policy_id": self.policy_id,
            "name": self.name,
            "ip_proto": self.ip_proto.compressed,
            "source_port": self.source_port,
        }


class ArupaRule(Rule):
    source_subnet: IPv4Network or IPv6Network

    def to_dict(self):
        rule_dict = super().to_dict()
        rule_dict["source_subnet"] = self.source_subnet.compressed
        return rule_dict


class FriscoRule(Rule):
    source_ip: IPv4Network or IPv6Network
    destination_ip: IPv4Network or IPv6Network

    def to_dict(self):
        rule_dict = super().to_dict()
        rule_dict.update({
            "source_ip": self.source_ip.compressed,
            "destination_ip": self.destination_ip.compressed,
        })
        return rule_dict
