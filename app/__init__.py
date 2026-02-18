import shutil
from time import time
from flask import Flask
from flask_session import Session
from app.main.routes import main


def create_app():
    app = Flask(__name__)

    app.secret_key = "dev-secret-key"

    SESSION_DIR = "/tmp/flask_sessions"

    # HARD RESET SESSIONS ON APP START
    shutil.rmtree(SESSION_DIR, ignore_errors=True)

    UPLOAD_DIR = "uploads"
#  STEP 3: CLEAR UPLOADED DOCUMENTS ON APP START
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)

    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_FILE_DIR"] = SESSION_DIR
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True

    Session(app)

    @app.before_request
    def track_activity():
        with open("/tmp/last_request.txt", "w") as f:
            f.write(str(time.time()))

    app.register_blueprint(main)
    return app
