import json
import uuid
from typing import List, Dict

from src.models.Policy import Policy, PolicyType
from src.utils.policy_utils import extract_json_from_string


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
            self.__is_valid_policy_on_create(json_input=json_input)
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
        # return jsonify({"error": f"Policy with ID {policy_id} not found"}), 404

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        policy_id = json_identifier
        policy = self.policies.get(policy_id)
        self.__is_valid_policy_on_update(json_input=json_input, policy_id=policy_id)
        updated_policy_fields = extract_json_from_string(json_input=json_input)
        updated_policy = Policy(
            id=policy_id,
            name=updated_policy_fields.get('name', policy.name),
            description=updated_policy_fields.get('description', policy.description),
            type=updated_policy_fields.get('type', policy.type)
        )
        self.policies[policy_id] = updated_policy

    def delete_policy(self, json_identifier: str) -> None:
        policy_id = json_identifier
        policy = self.policies.get(policy_id)
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        del self.policies[policy_id]

    def list_policies(self) -> str:
        return json.dumps(self.from_policy_to_json(policies=list(self.policies.values())))

    def __is_policy_name_exists(self, policy_name: str, policy_type: PolicyType) -> bool:
        """
        An Arupa policy may not have the same name as another Arupa policy.
        Multiple Frisco policies may have the same name.
        """
        return any(
            policy.name == policy_name and policy_type == PolicyType.ARUPA.value for policy in self.policies.values())

    def __is_valid_policy_on_create(self, json_input: str) -> None:
        policy_data = extract_json_from_string(json_input=json_input)
        required_fields = ['name', 'description', 'type']
        for field in required_fields:
            if field not in policy_data:
                raise ValueError(f"Missing required field: {field}")
        if not policy_data['name'].isalnum() or '_' in policy_data['name']:
            raise ValueError("Name must consist of alphanumeric characters and underscores only")

        policy_name_already_exists = self.__is_policy_name_exists(policy_name=policy_data['name'],
                                                                  policy_type=policy_data['type'])
        if policy_name_already_exists:
            raise ValueError(f"Policy name must be unique for '{PolicyType.ARUPA}'")

    def __is_valid_policy_on_update(self, policy_id: str, json_input) -> None:
        policy = self.policies.get(policy_id)
        if not policy_id or not json_input:
            raise ValueError("Both json_identifier and json_input are required.")
        if not policy:
            raise ValueError(f"Missing Policy by ID: {policy_id}")
        updated_policy_fields = extract_json_from_string(json_input=json_input)
        optional_fields = ['name', 'description', 'type']
        is_one_of_optional_fields_exists = False
        for field in optional_fields:
            if field in updated_policy_fields:
                is_one_of_optional_fields_exists = True
        if not is_one_of_optional_fields_exists:
            raise ValueError(f"There is nothing to update in this request")

        new_type = updated_policy_fields.get('type', None)
        new_name = updated_policy_fields.get('name', None)
        if new_type and not any(new_type == member.value for member in PolicyType):
            raise ValueError(f"Invalid policy type: {new_type}")
        new_type = updated_policy_fields.get('type', policy.type)
        if new_type and new_name and self.__is_policy_name_exists(policy_name=new_name, policy_type=new_type):
            raise ValueError(
                f"A policy with the name '{updated_policy_fields['name']}' already exists for type '{new_type}'.")

    @classmethod
    def from_policy_to_json(cls, policies: List[Policy]) -> str:
        return json.dumps([policy.to_dict() for policy in policies], indent=2)
