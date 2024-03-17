import json
from flask import request, Blueprint

from src.config.logger import setup_logger
from src.skeleton.stage3 import PolicyAPI

rule_api = PolicyAPI()
rule_bp = Blueprint('rule', __name__)
logger = setup_logger()


@rule_bp.route('/policies/<policy_id>/rules', methods=['POST'])
def create_rule_to_policy_route(policy_id):
    try:
        rule_data = request.get_data()
        created_rule = rule_api.create_rule(json_policy_identifier=policy_id, rule_data=rule_data)
        return created_rule, 201
    except ValueError as ex:
        logger.error('Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 400
    except Exception as ex:
        logger.error('Un maintained Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 500


@rule_bp.route('/policies/<policy_id>/rules', methods=['GET'])
def get_policy_rules_route(policy_id):
    try:
        return rule_api.list_rules(json_policy_identifier=json.dumps(policy_id)), 200
    except Exception as ex:
        logger.error('Un maintained Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 500


@rule_bp.route('/policies/<policy_id>/rules/<rule_id>', methods=['GET'])
def get_policy_rule_route(policy_id, rule_id):
    try:
        return rule_api.read_rule(
            json_identifier=json.dumps({"policy_id": policy_id, "rule_id": rule_id})), 200
    except Exception as ex:
        logger.error('Un maintained Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 500


@rule_bp.route('/policies/<policy_id>/rules/<rule_id>', methods=['PUT'])
def update_policy_rule_route(policy_id, rule_id):
    try:
        updated_rule_fields = request.get_data()
        rule_api.update_rule(
            json_identifier=json.dumps({"policy_id": policy_id, "rule_id": rule_id}),
            json_rule_input=updated_rule_fields
        )
        return f'Update successfully policy rule: {policy_id} - {rule_id}', 200
    except ValueError as ex:
        logger.error('Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 400
    except Exception as ex:
        logger.error('Un maintained Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 500


@rule_bp.route('/policies/<policy_id>/rules/<rule_id>', methods=['DELETE'])
def delete_policy_rule_route(policy_id, rule_id):
    try:
        rule_api.delete_rule(json_identifier=json.dumps({"policy_id": policy_id, "rule_id": rule_id}))
        return f'Delete successfully policy rule: {policy_id} - {rule_id}', 200
    except ValueError as ex:
        logger.error('Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 400
    except Exception as ex:
        logger.error('Un maintained Error occurred: %s', str(ex), exc_info=True)
        return {"error": str(ex)}, 500
