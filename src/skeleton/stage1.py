import json
import uuid
from typing import List

from src.models.Policy import Policy
from src.utils.policy_utils import extract_json_from_string, from_policy_to_json


class PolicyAPI:
    def __init__(self) -> None:
        self.policies: List[Policy] = []

    def create_policy(self, json_input: str) -> str:
        try:
            self.__is_valid_policy(json_input=json_input)
            policy_data = extract_json_from_string(json_input=json_input)
            policy = Policy(
                id=str(uuid.uuid4()),
                name=policy_data.get('name', None),
                description=policy_data.get('description', None)
            )
            self.policies.append(policy)
            return json.dumps({"id": policy.id})
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        except Exception as ex:
            raise ValueError(ex)

    def list_policies(self) -> str:
        policies = from_policy_to_json(policies=self.policies)
        return json.dumps(policies).replace('\n', '')

    def __is_valid_policy(self, json_input: str) -> bool:
        policy_data = extract_json_from_string(json_input=json_input)
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in policy_data:
                raise ValueError(f"Missing required field: {field}")
        if not policy_data['name'].isalnum() or '_' in policy_data['name']:
            raise ValueError("Name must consist of alphanumeric characters and underscores only")

        if any(policy.name == policy_data['name'] for policy in self.policies):
            raise ValueError("Policy name must be unique")
