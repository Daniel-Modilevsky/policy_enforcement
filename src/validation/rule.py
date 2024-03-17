from typing import Dict, List

from src.models.policy import PolicyType, Policy
from src.models.rule import Rule
from src.utils.policy_utils import extract_json_from_string

def is_rule_name_available(rule_name: str, policy_type: PolicyType, rules: Dict[str, List[Rule]]) -> bool:
    """
    Arupa rule names must be unique within each policy.
    Frisco rule names must be globally unique, even between policies.
    """
    existing_rules_with_same_name = []
    for policy_id, rules_list in rules.items():
        for rule in rules_list:
            if rule.name == rule_name:
                existing_rules_with_same_name.append(rule)

    if len(existing_rules_with_same_name) == 0:
        return True

    if len(existing_rules_with_same_name) > 0 and policy_type == PolicyType.FRISCO:
        return False
    return True


def is_valid_rule_on_create(json_input: str, policy_id: str, policies: Dict[str, Policy], rules) -> None:
    rule_data = extract_json_from_string(json_input=json_input)
    required_fields = ['name', 'ip_proto', 'source_port']
    for field in required_fields:
        if field not in rule_data:
            raise ValueError(f"Missing required field: {field}")
    policy = policies.get(policy_id)
    rule_name_available = is_rule_name_available(rule_name=rule_data['name'], policy_type=policy.type, rules=rules)
    if not rule_name_available:
        raise ValueError(
            f"Rule name must be unique globally for '{PolicyType.FRISCO}' and unique by policy for '{PolicyType.ARUPA}'")


def is_valid_rule_on_update(json_input: str, policy_id: str, policies: Dict[str, Policy],
                            rules: Dict[str, List[Rule]]) -> None:
    rule_data = extract_json_from_string(json_input=json_input)
    optional_fields = ['name', 'ip_proto', 'source_port']
    is_one_of_optional_fields_exists = False
    for field in optional_fields:
        if field in rule_data:
            is_one_of_optional_fields_exists = True
    if not is_one_of_optional_fields_exists:
        raise ValueError(f"There is nothing to update in this request")
    policy = policies.get(policy_id)
    rule_name_available = is_rule_name_available(rule_name=rule_data['name'], policy_type=policy.type, rules=rules)
    if not rule_name_available:
        raise ValueError(
            f"Rule name must be unique globally for '{PolicyType.FRISCO}' and unique by policy for '{PolicyType.ARUPA}'")