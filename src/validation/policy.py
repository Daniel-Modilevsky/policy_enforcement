from typing import Dict

from src.models.policy import PolicyType, Policy
from src.utils.policy_utils import extract_json_from_string


def is_policy_name_exists(policy_name: str, policy_type: PolicyType, policies: Dict[str, Policy]) -> bool:
    """
    An Arupa policy may not have the same name as another Arupa policy.
    Multiple Frisco policies may have the same name.
    """
    return any(
        policy.name == policy_name and policy_type == PolicyType.ARUPA.value for policy in policies.values())


def is_policy_has_all_parameters_on_create(policy_data: dict) -> bool:
    required_fields = ['name', 'description', 'type']
    for field in required_fields:
        if field not in policy_data:
            return False
    return True


def is_policy_has_at_least_one_parameter(updated_policy_fields: dict) -> bool:
    optional_fields = ['name', 'description', 'type']
    for field in optional_fields:
        if field in updated_policy_fields:
            return True
    return False


def is_name_contain_not_alphanumeric_characters(name: str) -> bool:
    return name.isalnum() or '_' in name


def validate_policy_on_create(json_input: str, policies: Dict[str, Policy]) -> None:
    policy_data = extract_json_from_string(json_input=json_input)
    if not is_policy_has_all_parameters_on_create(policy_data):
        raise ValueError(f"Missing required fields in policy")
    if not is_name_contain_not_alphanumeric_characters(policy_data['name']):
        raise ValueError("Name must consist of alphanumeric characters and underscores only")
    policy_name_already_exists = is_policy_name_exists(policy_name=policy_data['name'],
                                                       policy_type=policy_data['type'], policies=policies)
    if policy_name_already_exists:
        raise ValueError(f"Policy name must be unique for '{PolicyType.ARUPA}'")


def is_policy_type_valid(policy_type) -> bool:
    return policy_type and not any(policy_type == member.value for member in PolicyType)


def validate_policy_on_update(policy_id: str, json_input, policies: Dict[str, Policy]) -> None:
    policy = policies.get(policy_id)
    if not policy_id or not json_input:
        raise ValueError("Both json_identifier and json_input are required.")
    if not policy:
        raise ValueError(f"Missing Policy by ID: {policy_id}")
    updated_policy_fields = extract_json_from_string(json_input=json_input)
    if not is_policy_has_at_least_one_parameter(updated_policy_fields):
        raise ValueError(f"There is nothing to update in this request")

    updated_policy_type = updated_policy_fields.get('type', None)
    updated_policy_name = updated_policy_fields.get('name', None)
    if not updated_policy_type or updated_policy_name:
        return
    if not is_policy_type_valid(updated_policy_type):
        raise ValueError(f"Invalid policy type: {updated_policy_type}")
    if updated_policy_type and updated_policy_name and is_policy_name_exists(policy_name=updated_policy_name, policy_type=updated_policy_type):
        raise ValueError(
            f"A policy with the name '{updated_policy_fields['name']}' already exists for type '{updated_policy_type}'.")
