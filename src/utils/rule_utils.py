import uuid
from typing import Dict, List

from src.models.policy import PolicyType, Policy
from src.models.rule import Rule, ArupaRule, FriscoRule
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


def classify_rule_type(json_input: str, policy_type: PolicyType) -> PolicyType:
    rule_data = extract_json_from_string(json_input=json_input)
    source_subnet = rule_data.get('source_subnet', None)
    destination_ip = rule_data.get('destination_ip', None)
    source_ip = rule_data.get('source_ip', None)
    if source_subnet is not None and policy_type == PolicyType.ARUPA:
        return PolicyType.ARUPA
    if source_ip is not None and destination_ip is not None and policy_type == PolicyType.FRISCO:
        return PolicyType.FRISCO
    return PolicyType.DEFAULT


def create_rule_by_policy_type(rule_type: PolicyType, rule_data_as_json: dict, policy_id: str) -> Rule:
    if rule_type == PolicyType.ARUPA:
        return ArupaRule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', None),
            ip_proto=rule_data_as_json.get('ip_proto', None),
            source_port=rule_data_as_json.get('source_port', None),
            source_subnet=rule_data_as_json.get('source_subnet', None)
        )
    elif rule_type == PolicyType.FRISCO:
        return FriscoRule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', None),
            ip_proto=rule_data_as_json.get('ip_proto', None),
            source_port=rule_data_as_json.get('source_port', None),
            source_ip=rule_data_as_json.get('source_ip', None),
            destination_ip=rule_data_as_json.get('destination_ip', None)
        )
    else:
        return Rule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', None),
            ip_proto=rule_data_as_json.get('ip_proto', None),
            source_port=rule_data_as_json.get('source_port', None)
        )


def update_rule_by_policy_type(rule_type: PolicyType, rule_data_as_json: dict, policy_id: str, old_rule: Rule) -> Rule:
    if rule_type == PolicyType.ARUPA:
        return ArupaRule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', old_rule.name),
            ip_proto=rule_data_as_json.get('ip_proto', old_rule.ip_proto),
            source_port=rule_data_as_json.get('source_port', old_rule.source_port),
            source_subnet=rule_data_as_json.get('source_subnet', None)
        )
    elif rule_type == PolicyType.FRISCO:
        return FriscoRule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', old_rule.name),
            ip_proto=rule_data_as_json.get('ip_proto', old_rule.ip_proto),
            source_port=rule_data_as_json.get('source_port', old_rule.source_port),
            source_ip=rule_data_as_json.get('source_ip', None),
            destination_ip=rule_data_as_json.get('destination_ip', None)
        )
    else:
        return Rule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', old_rule.name),
            ip_proto=rule_data_as_json.get('ip_proto', old_rule.ip_proto),
            source_port=rule_data_as_json.get('source_port', old_rule.source_port)
        )
