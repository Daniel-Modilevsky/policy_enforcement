from pydantic import BaseModel, constr
from enum import Enum


class PolicyType(Enum):
    ARUPA = 'Arupa'
    FRISCO = 'Frisco'
    DEFAULT = 'Default'


class Policy(BaseModel):
    id: str
    name: constr(min_length=1, max_length=32)
    description: constr(min_length=0)
    type: PolicyType

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            type=PolicyType[data["type"]],
        )
