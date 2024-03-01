from flask import Flask, request
from config.logger import setup_logger
from src.skeleton.stage1 import PolicyAPI

app = Flask(__name__)
logger = setup_logger()


policy_api = PolicyAPI()


@app.route('/')
def entry_route():
    logger.info('API call: / endpoint accessed')
    return 'Policy Enforcement Assessment'


@app.route('/policies', methods=['POST'])
def create_policy_route():
    try:
        policy_data = request.get_data()
        created_policy = policy_api.create_policy(policy_data)
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


if __name__ == "__main__":
    app.run()
