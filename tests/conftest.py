import json
import pytest
from src.skeleton.stage3 import PolicyAPI


@pytest.fixture
def api():
    return PolicyAPI()


@pytest.fixture
def foo_policy_identifier(api):
    return api.create_policy(
        json.dumps(
            {
                "name": "foo",
                "description": "my foo policy",
                "type": "Arupa",
            }
        )
    )


@pytest.fixture
def bar_policy_identifier(api):
    return api.create_policy(
        json.dumps(
            {
                "name": "bar",
                "description": "my bar policy",
                "type": "Arupa",
            }
        )
    )


@pytest.fixture
def rule_policy_identifier_daniel(api):
    policy = api.create_policy(
        json.dumps(
            {
                "name": "daniel",
                "description": "my daniel policy",
                "type": "Arupa",
            }
        )
    )
    policy_id = json.loads(policy)
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
    return json.dumps({"policy_id": policy_id, "rule_id": rule.get('id')})


@pytest.fixture
def rule_policy_identifier_michael(api):
    policy = api.create_policy(
        json.dumps(
            {
                "name": "michael",
                "description": "michael policy",
                "type": "Arupa",
            }
        )
    )
    policy_id = json.loads(policy)
    rule_str = api.create_rule(
        policy_id,
        json.dumps(
            {
                "name": "Generic Rule 2",
                "ip_proto": "192.168.0.0/24",
                "source_ip": "192.168.0.0/24",
                "destination_ip": "192.168.0.0/24",
                "source_port": 80
            }
        )
    )
    rule = json.loads(rule_str)
    return json.dumps({"policy_id": policy_id, "rule_id": rule.get('id')})
