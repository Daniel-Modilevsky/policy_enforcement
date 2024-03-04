# Policy Enforcement System

## Introduction

This is a Python implementation of a programmatic CRUD interface for managing network policies and rules. 
The system allows defining policies and rules, enforcing restrictions, and performing various operations on them.


## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Requirements

- Python 3.6 or above
- Poetry

## Installation

```bash
- Clone the repository to your local machine.
- Open a terminal window and navigate to the root directory of the cloned repository.
  $ python3 -m venv venv
  $ . venv/bin/activate
  $ poetry install
```

## Usage

```bash
  $ poetry run python src/main.py
  - This command will start the application server. 
  - Open the browser and navigate to http://localhost:5000.
```


## Documentation

### Classes

- PolicyAPI: The main class responsible for managing policies and rules.
- Policy: Is a group of definitions of what traffic is allowed or forbidden.
- Rule: Is one of the definitions specifying a type of network traffic.


### API Endpoints

- GET '/' - Application entry.

- GET '/policies' - Get policies.
- POST '/policies' - Create new policy.
- GET '/policies/<policy_id>' - Get policy.
- PUT '/policies/<policy_id>' - Update policy.
- DELETE '/policies/<policy_id>' - Delete policy.

- GET '/policies/<policy_id>/rules' - Get policy rules.
- POST '/policies/<policy_id>/rules' - Create new policy.
- GET '/policies/<policy_id>/rules<rule_id>' - Get policy rule.
- PUT '/policies/<policy_id>/rules<rule_id>' - Update policy rule.
- DELETE '/policies/<policy_id>/rules<rule_id>' - Delete policy rule.


### Methods:

- create_policy(json_policy_data: str) -> str: Creates a new policy.
- list_policies() -> str: Lists all policies.
- read_policy(json_policy_identifier: str) -> str: Read a specific policy.
- update_policy(json_policy_identifier: str, json_policy_input: str) -> None: Update an existing policy.
- delete_policy(json_policy_identifier: str) -> None: Delete a policy.

- create_rule(json_policy_identifier: str, json_rule_input: str) -> str: Create a new rule to policy.
- read_rule(json_rule_identifier: str) -> str: Read a specific rule of policy.
- update_rule(json_rule_identifier: str, json_rule_input: str) -> None: Update an existing rule of policy.
- delete_rule(json_rule_identifier: str) -> None: Delete a rule of policy.
- list_rules(json_policy_identifier: str) -> str: Lists all rules associated with a policy.

### Examples

- POST '/policies' - Create new policy 
```bash
  {"name": "foo", "description": "my foo policy", "type": "Frisco"}
```

- PUT '/policies/<policy_id>' - Update policy.
```bash
  {"name": "updated_foo", "description": "updated_my foo policy", "type": "Arupa"}
```

- POST '/policies/<policy_id>/rules' - Create new policy.
```bash
  {"name": "Generic Rule", "ip_proto": "192.168.0.0/24","source_ip":"192.168.0.0/24" ,"destination_ip": "192.168.0.0/24", "source_port": 80}
```

- PUT '/policies/<policy_id>/rules<rule_id>' - Update policy rule.
```bash
  {"name": "Updated Generic Rule", "ip_proto": "192.168.0.0/24", "source_port": 8080}
```

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, 
please open an issue or create a pull request.

Best,
Daniel Modilevsky