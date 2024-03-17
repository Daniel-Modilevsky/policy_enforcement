import json


class TestReadPolicyRule:
    def test_returns_valid_json(self, api, rule_policy_identifier_daniel):
        rule = json.loads(api.read_rule(rule_policy_identifier_daniel))
        assert rule

    def test_returns_dict_with_fields(self, api, rule_policy_identifier_daniel):
        rule = json.loads(api.read_rule(rule_policy_identifier_daniel))
        assert isinstance(rule, dict)
        assert rule["name"] == "Generic Rule"
        assert rule["ip_proto"] == "192.168.0.0/24"
        assert rule["destination_ip"] == "192.168.0.0/24"
        assert rule["source_port"] == 80

    # def test_invalid_or_nonexistent_identifier(self, api):
    #     with pytest.raises(Exception):
    #         api.read_policy(json.dumps("invalid"))
    #
    # def test_consistent_response_for_same_policy(self, api, foo_policy_identifier):
    #     assert api.read_policy(foo_policy_identifier) == api.read_policy(
    #         foo_policy_identifier
    #     )
    #
    # def test_different_response_for_different_policies(
    #         self, api, foo_policy_identifier, bar_policy_identifier
    # ):
    #     assert api.read_policy(foo_policy_identifier) != api.read_policy(
    #         bar_policy_identifier
    #     )
