import json
from typing import List

from src.models.policy import Policy


def extract_json_from_string(json_input: str) -> dict:
    try:
        json_data = json.loads(json_input)
        if isinstance(json_data, dict):
            return json_data
    except json.JSONDecodeError as ex:
        raise ValueError(f"Invalid JSON format: {ex}")


def from_policy_to_json(policies: List[Policy]) -> str:
    return json.dumps([policy.to_dict() for policy in policies], indent=2)
