from flask import Flask, request
from config.logger import setup_logger
from src.skeleton.stage2 import PolicyAPI

app = Flask(__name__)
logger = setup_logger()

policy_api = PolicyAPI()


@app.route('/')
def entry_route():
    logger.info('API call: / endpoint accessed')
    return 'Policy Enforcement Assessment'


# TODO: change the error status code
@app.route('/policies', methods=['POST'])
def create_policy_route():
    try:
        policy_data = request.get_data()
        created_policy = policy_api.create_policy(json_input=policy_data)
        return created_policy, 201

    except Exception as ex:
        logger.error('Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 400


@app.route('/policies', methods=['GET'])
def list_policies_route():
    try:
        policies_list = policy_api.list_policies()
        return policies_list
    except Exception as ex:
        logger.error('Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 400


@app.route('/policies/<policy_id>', methods=['GET'])
def get_policy_route(policy_id):
    try:
        return policy_api.read_policy(json_identifier=policy_id)
    except Exception as ex:
        logger.error('Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 400


@app.route('/policies/<policy_id>', methods=['PUT'])
def update_policy_route(policy_id):
    try:
        updated_policy_data = request.get_json()
        return policy_api.update_policy(policy_id, updated_policy_data)
    except Exception as ex:
        logger.error('Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 400


@app.route('/policies/<policy_id>', methods=['DELETE'])
def delete_policy_route(policy_id):
    try:
        return policy_api.delete_policy(policy_id)
    except Exception as ex:
        logger.error('Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 400


if __name__ == "__main__":
    app.run()
