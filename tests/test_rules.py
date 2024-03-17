import json

import pytest


class TestReadPolicyRule:
    def test_returns_valid_json(self, api, rule_policy_identifier_daniel):
        rule = json.loads(api.read_rule(rule_policy_identifier_daniel))
        assert rule

    def test_returns_dict_with_fields(self, api, rule_policy_identifier_daniel):
        rule = json.loads(api.read_rule(rule_policy_identifier_daniel))
        assert isinstance(rule, dict)
        assert rule["name"] == "Generic Rule"
        assert rule["ip_proto"] == "192.168.0.0/24"
        assert rule["source_port"] == 80

    def test_invalid_or_nonexistent_identifier(self, api):
        with pytest.raises(Exception):
            api.read_rule(json.dumps("invalid"))

    def test_consistent_response_for_same_rule(self, api, rule_policy_identifier_daniel):
        assert api.read_rule(rule_policy_identifier_daniel) == api.read_rule(
            rule_policy_identifier_daniel
        )

    def test_different_response_for_different_rules(
            self, api, rule_policy_identifier_daniel, rule_policy_identifier_michael
    ):
        assert api.read_rule(rule_policy_identifier_daniel) != api.read_rule(
            rule_policy_identifier_michael
        )


class TestCreatePolicyRule:
    def test_create_valid_rules_with_same_name(self, api, foo_policy_identifier):
        policy_id = json.loads(foo_policy_identifier)
        rule_str = api.create_rule(
            policy_id,
            json.dumps(
                {
                    "name": "Generic Rule",
                    "ip_proto": "192.168.0.0/24",
                    "source_ip": "192.168.0.0/24",
                    "destination_ip": "192.168.0.0/24",
                    "source_port": 80
                }
            )
        )
        rule = json.loads(rule_str)
        rule_str = api.create_rule(
            policy_id,
            json.dumps(
                {
                    "name": "Generic Rule",
                    "ip_proto": "192.168.0.0/24",
                    "source_ip": "192.168.0.0/24",
                    "destination_ip": "192.168.0.0/24",
                    "source_port": 80
                }
            )
        )
        rule2 = json.loads(rule_str)
        assert rule
        assert rule2


class TestListPolicyRules:
    def test_list_one(self, api, rule_policy_identifier_daniel):
        rule_data = json.loads(rule_policy_identifier_daniel)
        policy_id = rule_data.get('policy_id', None)
        rule_id = rule_data.get('rule_id', None)
        policy = json.loads(api.read_policy(json.dumps(policy_id)))
        assert policy
        rules = json.loads(api.list_rules(json.dumps(policy_id)))
        assert len(rules) == 1
        [rule] = rules
        assert isinstance(policy, dict)
        assert rule["name"] == 'Generic Rule'
        assert rule["id"] == rule_id


class TestDeletePolicyRule:
    def test_no_read_after_delete(self, api, rule_policy_identifier_daniel):
        api.read_rule(rule_policy_identifier_daniel)
        api.delete_rule(rule_policy_identifier_daniel)
        with pytest.raises(Exception):
            api.read_policy(rule_policy_identifier_daniel)
