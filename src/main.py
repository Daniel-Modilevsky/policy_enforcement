from flask import Flask

from src.routes.policy import policy_bp
from src.routes.rule import rule_bp

app = Flask(__name__)

app.register_blueprint(policy_bp)
app.register_blueprint(rule_bp)

if __name__ == "__main__":
    app.run()
