import json
from typing import List
from src.models.policy import Policy

LOOP_TRASH_HOLD = 5



def extract_json_from_string(json_input: str) -> dict:
    for index in range(LOOP_TRASH_HOLD):
        try:
            json_data = json.loads(json_input)
            if isinstance(json_data, dict):
                return json_data
            json_input = json_data
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON format")
