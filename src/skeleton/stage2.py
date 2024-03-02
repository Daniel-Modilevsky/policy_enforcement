import json
import uuid
from typing import List, Dict

from src.models.Policy import Policy, PolicyType
from src.utils.policy_utils import extract_json_from_string


# todo: all the is function change to boolean, and the controller will raise the exception
# All the changes that can be in phase 1 move to there.

class PolicyAPI:
    def __init__(self) -> None:
        """
         Using Dict instead of a List.
         The actions of the read 1 Policy, update and delete will be O(1).
         Get all policies will still be O(n) like in a list.
        """
        self.policies: Dict[str, Policy] = {}

    def create_policy(self, json_input: str) -> str:
        try:
            self.__is_valid_policy(json_input=json_input)
            policy_data = extract_json_from_string(json_input=json_input)
            policy = Policy(
                id=str(uuid.uuid4()),
                name=policy_data.get('name', None),
                description=policy_data.get('description', None),
                type=policy_data.get('type', None)
            )
            self.policies[policy.id] = policy
            return json.dumps(policy.id)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        except Exception as ex:
            raise ValueError(ex)

    def read_policy(self, json_identifier: str) -> str:
        policy_id = json_identifier
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        return json.dumps(policy.to_dict())
        # if policy_id in self.policies:
        # Update the policy with the new data
        # return self.policies2.get(policy_id, None)
        #         if policy:
        #             return policy
        #         else:
        #             return jsonify({"error": f"Policy with ID {policy_id} not found"}), 404

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        # if policy_id in self.policies:
        #     # Update the policy with the new data
        #     self.policies2[policy_id] = updated_policy
        raise NotImplementedError

    def delete_policy(self, json_identifier: str) -> None:
        # if policy_id in self.policies:
        #     # Remove the policy with the given ID
        #     del self.policies2[policy_id]
        raise NotImplementedError

    def list_policies(self) -> str:
        return json.dumps(self.from_policy_to_json(policies=list(self.policies.values())))

    def __is_policy_name_exists(self, policy_name: str, policy_type: PolicyType) -> None:
        '''
        An Arupa policy may not have the same name as another Arupa policy.
        Multiple Frisco policies may have the same name.
        '''
        # todo: maybe store all the names in dict to get names in O(1)
        if any(policy.name == policy_name and policy_type == PolicyType.ARUPA.value for policy in self.policies):
            raise ValueError(f"Policy name must be unique for '{PolicyType.ARUPA}'")

    def __is_valid_policy(self, json_input: str) -> None:
        policy_data = extract_json_from_string(json_input=json_input)
        required_fields = ['name', 'description', 'type']
        for field in required_fields:
            if field not in policy_data:
                raise ValueError(f"Missing required field: {field}")
        if not policy_data['name'].isalnum() or '_' in policy_data['name']:
            raise ValueError("Name must consist of alphanumeric characters and underscores only")

        self.__is_policy_name_exists(policy_name=policy_data['name'], policy_type=policy_data['type'])

    @classmethod
    def from_policy_to_json(cls, policies: List[Policy]) -> str:
        return json.dumps([policy.to_dict() for policy in policies], indent=2)
