# Each policy is associated with a set of rules.
# A rule is one of the definitions specifying a type of network traffic. Rules for Arupa policies and Frisco policies are different.
# Each Arupa rule has the following fields:
# name - free text
# ip_proto - an IP protocol number source_port - a port number source_subnet - an IP subnet
# Arupa rule names must be unique within each policy. Each Frisco rule has the following fields:
# name - free text
# ip_proto - an IP protocol number source_port - a port number source_ip - an IP address destination_ip - an IP address
# Frisco rule names must be globally unique, even between policies.


from pydantic import BaseModel, constr
from ipaddress import IPv4Network, IPv6Network


# todo: manage the names separately?
# if this was db the index was also by name
# Frisco rule names must be globally unique, even between policies.

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

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            policy_id=data["policy_id"],
            name=data["name"],
            ip_proto=IPv4Network(data["ip_proto"]) if '/' in data["ip_proto"] else IPv6Network(data["ip_proto"]),
            source_port=data["source_port"],
        )


class ArupaRule(Rule):
    source_subnet: IPv4Network or IPv6Network

    def to_dict(self):
        rule_dict = super().to_dict()
        rule_dict["source_subnet"] = self.source_subnet.compressed
        return rule_dict

    @classmethod
    def from_dict(cls, data):
        source_subnet = IPv4Network(data["source_subnet"]) if '/' in data["source_subnet"] else IPv6Network(
            data["source_subnet"])
        return cls(source_subnet=source_subnet, **data)


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

    @classmethod
    def from_dict(cls, data):
        source_ip = IPv4Network(data["source_ip"]) if '/' in data["source_ip"] else IPv6Network(data["source_ip"])
        destination_ip = IPv4Network(data["destination_ip"]) if '/' in data["destination_ip"] else IPv6Network(
            data["destination_ip"])
        return cls(source_ip=source_ip, destination_ip=destination_ip, **data)
