import json
from typing import Dict, List

from src.models.policy import PolicyType, Policy


def extract_json_from_string(json_input: str) -> dict:
    try:
        json_data = json.loads(json_input)
        if isinstance(json_data, dict):
            return json_data
    except json.JSONDecodeError as ex:
        raise ValueError(f"Invalid JSON format: {ex}")


def is_policy_name_exists(policy_name: str, policy_type: PolicyType, policies: Dict[str, Policy]) -> bool:
    """
    An Arupa policy may not have the same name as another Arupa policy.
    Multiple Frisco policies may have the same name.
    """
    return any(
        policy.name == policy_name and policy_type == PolicyType.ARUPA.value for policy in policies.values())


def is_valid_policy_on_create(json_input: str, policies: Dict[str, Policy]) -> None:
    policy_data = extract_json_from_string(json_input=json_input)
    required_fields = ['name', 'description', 'type']
    for field in required_fields:
        if field not in policy_data:
            raise ValueError(f"Missing required field: {field}")
    if not policy_data['name'].isalnum() or '_' in policy_data['name']:
        raise ValueError("Name must consist of alphanumeric characters and underscores only")

    policy_name_already_exists = is_policy_name_exists(policy_name=policy_data['name'],
                                                       policy_type=policy_data['type'], policies=policies)
    if policy_name_already_exists:
        raise ValueError(f"Policy name must be unique for '{PolicyType.ARUPA}'")


def is_valid_policy_on_update(policy_id: str, json_input, policies: Dict[str, Policy]) -> None:
    policy = policies.get(policy_id)
    if not policy_id or not json_input:
        raise ValueError("Both json_identifier and json_input are required.")
    if not policy:
        raise ValueError(f"Missing Policy by ID: {policy_id}")
    updated_policy_fields = extract_json_from_string(json_input=json_input)
    optional_fields = ['name', 'description', 'type']
    is_one_of_optional_fields_exists = False
    for field in optional_fields:
        if field in updated_policy_fields:
            is_one_of_optional_fields_exists = True
    if not is_one_of_optional_fields_exists:
        raise ValueError(f"There is nothing to update in this request")

    new_type = updated_policy_fields.get('type', None)
    new_name = updated_policy_fields.get('name', None)
    if not new_type or new_name:
        return
    if new_type and not any(new_type == member.value for member in PolicyType):
        raise ValueError(f"Invalid policy type: {new_type}")
    new_type = updated_policy_fields.get('type', policy.type)
    if new_type and new_name and is_policy_name_exists(policy_name=new_name, policy_type=new_type):
        raise ValueError(
            f"A policy with the name '{updated_policy_fields['name']}' already exists for type '{new_type}'.")


def from_policy_to_json(policies: List[Policy]) -> str:
    return json.dumps([policy.to_dict() for policy in policies], indent=2)
