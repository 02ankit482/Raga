from flask import Flask
from app.main.routes import main


def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"  # change later for prod
    app.config["RESET_CHAT_ON_STARTUP"] = True
    app.register_blueprint(main)
    return app
