import json
import uuid

from flask import Flask, request

from config.logger import setup_logger

app = Flask(__name__)
logger = setup_logger()


class PolicyAPI:
    def __init__(self) -> None:
        self.policies = []
        pass

    def create_policy(self, json_input: str) -> str:
        try:
            policy_data = json.loads(json_input)
            required_fields = ['name', 'description']
            for field in required_fields:
                if field not in policy_data:
                    raise ValueError(f"Missing required field: {field}")

            # Put in class with validation like the filters
            if len(policy_data['name']) > 32:
                raise ValueError("Name must be at most 32 characters")

            # Use package for that
            if not policy_data['name'].isalnum() or '_' in policy_data['name']:
                raise ValueError("Name must consist of alphanumeric characters and underscores only")

            if any(policy['name'] == policy_data['name'] for policy in self.policies):
                raise ValueError("Policy name must be unique")

            policy_id = str(uuid.uuid4())
            policy_data['id'] = policy_id

            self.policies.append(policy_data)
            return json.dumps({"id": policy_id})


        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        except Exception as ex:
            raise ValueError(ex)

    def list_policies(self) -> str:
        return json.dumps(self.policies)


policy_api = PolicyAPI()


@app.route('/')
def hello_world():
    logger.info('API call: / endpoint accessed')
    return 'Policy Enforcement Assessment'


@app.route('/policies', methods=['POST'])
def create_policy_route():
    try:
        policy_data = request.get_data(as_text=True)
        created_policy = policy_api.create_policy(policy_data)
        return created_policy, 201

    except ValueError as e:
        logger.error('Error occurred: %s', str(e), exc_info=True)
        return {"error": str(e)}, 400


@app.route('/policies', methods=['GET'])
def list_policies_route():
    policies_list = policy_api.list_policies()
    return policies_list


if __name__ == "__main__":
    app.run()
