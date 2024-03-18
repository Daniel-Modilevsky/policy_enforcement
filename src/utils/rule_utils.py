import uuid

from src.models.policy import PolicyType
from src.models.rule import Rule, ArupaRule, FriscoRule
from src.utils.policy_utils import extract_json_from_string


def classify_rule_type(json_input: str, policy_type: PolicyType) -> PolicyType:
    rule_data = extract_json_from_string(json_input=json_input)
    source_subnet = rule_data.get('source_subnet', None)
    destination_ip = rule_data.get('destination_ip', None)
    source_ip = rule_data.get('source_ip', None)
    if source_subnet is not None and policy_type == PolicyType.ARUPA:
        return PolicyType.ARUPA
    if source_ip is not None and destination_ip is not None and policy_type == PolicyType.FRISCO:
        return PolicyType.FRISCO
    raise ValueError("Invalid policy type, or policy type is not equal to rule type properties")


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
    raise ValueError('Missing required fields to create Rule')


def update_rule_by_policy_type(rule_type: PolicyType, rule_data_as_json: dict, policy_id: str, old_rule: Rule) -> Rule:
    if rule_type == PolicyType.ARUPA:
        return ArupaRule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', old_rule.get('name')),
            ip_proto=rule_data_as_json.get('ip_proto', old_rule.get('ip_proto')),
            source_port=rule_data_as_json.get('source_port', old_rule.get('source_port')),
            source_subnet=rule_data_as_json.get('source_subnet', None)
        )
    elif rule_type == PolicyType.FRISCO:
        return FriscoRule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', old_rule.get('name')),
            ip_proto=rule_data_as_json.get('ip_proto', old_rule.get('ip_proto')),
            source_port=rule_data_as_json.get('source_port', old_rule.get('source_port')),
            source_ip=rule_data_as_json.get('source_ip', None),
            destination_ip=rule_data_as_json.get('destination_ip', None)
        )
    raise ValueError('Missing required fields to update Rule')
