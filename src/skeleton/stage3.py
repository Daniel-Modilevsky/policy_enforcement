import json
import uuid
from typing import List, Dict

from src.models.policy import Policy
from src.models.rule import Rule
from src.utils.policy_utils import extract_json_from_string, is_valid_policy_on_create, is_valid_policy_on_update, \
    from_policy_to_json
from src.utils.rule_utils import is_valid_rule_on_create, is_valid_rule_on_update


# todo: rule type by the fields, if I got x + y it is a and if i got w + u it is b. (create and update)


class PolicyAPI:
    def __init__(self) -> None:
        """
         Using Dict instead of a List.
         The actions of the read 1 Policy, update and delete will be O(1).
         Get all policies will still be O(n) like in a list.
        """
        self.policies: Dict[str, Policy] = {}
        self.rules: Dict[str, List[Rule]] = {}

    def create_policy(self, json_input: str) -> str:
        try:
            is_valid_policy_on_create(json_input=json_input, policies=self.policies)
            policy_data = extract_json_from_string(json_input=json_input)
            policy = Policy(
                id=str(uuid.uuid4()),
                name=policy_data.get('name', None),
                description=policy_data.get('description', None),
                type=policy_data.get('type', None),
            )
            self.policies[policy.id] = policy
            return json.dumps(policy.id)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        except Exception as ex:
            raise ValueError(ex)

    def read_policy(self, json_identifier: str) -> str:
        policy_id = json.loads(json_identifier)
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        return json.dumps(policy.to_dict())

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        policy_id = json.loads(json_identifier)
        policy = self.policies.get(policy_id)
        is_valid_policy_on_update(json_input=json_input, policy_id=policy_id, policies=self.policies)
        updated_policy_fields = extract_json_from_string(json_input=json_input)
        updated_policy = Policy(
            id=policy_id,
            name=updated_policy_fields.get('name', policy.name),
            description=updated_policy_fields.get('description', policy.description),
            type=updated_policy_fields.get('type', policy.type),
        )
        self.policies[policy_id] = updated_policy

    def delete_policy(self, json_identifier: str) -> None:
        policy_id = json.loads(json_identifier)
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        del self.policies[policy_id]

    def list_policies(self) -> str:
        return from_policy_to_json(policies=list(self.policies.values()))

    def create_rule(self, json_policy_identifier: str, rule_data: str) -> str:
        policy_id = json_policy_identifier
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        rule_data_as_json = extract_json_from_string(json_input=rule_data)
        is_valid_rule_on_create(json_input=rule_data, policy_id=policy_id, policies=self.policies, rules=self.rules)
        rule = Rule(
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            name=rule_data_as_json.get('name', None),
            ip_proto=rule_data_as_json.get('ip_proto', None),
            source_port=rule_data_as_json.get('source_port', None)
        )

        if rule.policy_id not in self.rules:
            self.rules[rule.policy_id] = []
        self.rules[rule.policy_id].append(rule)
        return json.dumps(rule.to_dict())

    def read_rule(self, json_identifier: str) -> str:
        rule_data = extract_json_from_string(json_input=json_identifier)
        policy_id = rule_data.get('policy_id', None)
        rule_id = rule_data.get('rule_id', None)
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        return json.dumps(next((rule.to_dict() for rule in self.rules.get(policy_id, []) if rule.id == rule_id), None))

    def update_rule(self, json_identifier: str, json_rule_input: str) -> None:
        rule_data = extract_json_from_string(json_input=json_identifier)
        policy_id = rule_data.get('policy_id', None)
        rule_id = rule_data.get('rule_id', None)
        updated_rule_fields = extract_json_from_string(json_input=json_rule_input)
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        rule = next((rule.to_dict() for rule in self.rules.get(policy_id, []) if rule.id == rule_id), None)
        if not rule:
            raise ValueError(f"Missing rule by ID: {rule_id}")
        is_valid_rule_on_update(json_input=json_rule_input, policy_id=policy_id, policies=self.policies,
                                rules=self.rules)
        updated_rule = Rule(
            id=rule_id,
            policy_id=policy_id,
            name=updated_rule_fields.get('name', rule.get('name')),
            ip_proto=updated_rule_fields.get('ip_proto', rule.get('ip_proto')),
            source_port=updated_rule_fields.get('source_port', rule.get('source_port')),
        )
        self.rules[policy_id].pop(id == rule_id)
        self.rules[policy_id].append(updated_rule)

    def delete_rule(self, json_identifier: str) -> None:
        rule_data = extract_json_from_string(json_input=json_identifier)
        policy_id = rule_data.get('policy_id', None)
        rule_id = rule_data.get('rule_id', None)
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        rule = next((rule.to_dict() for rule in self.rules.get(policy_id, []) if rule.id == rule_id), None)
        if not rule:
            raise ValueError(f"Missing rule by ID: {rule_id}")
        self.rules[policy_id].pop(id == rule_id)

    def list_rules(self, json_policy_identifier: str) -> str:
        policy_id = json.loads(json_policy_identifier)
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        rules_list = [rule.to_dict() for rule in self.rules[policy_id]]
        return json.dumps(rules_list)
