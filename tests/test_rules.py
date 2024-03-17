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
