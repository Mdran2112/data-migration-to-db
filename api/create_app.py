import os

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from api import DB_CLIENT
from api.csv_watcher import CSVWatcher
from utils import CSV_DIRECTORY_PATH


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Employees REST API"
    app.config["API_VERSION"] = os.getenv("API_VERSION", "dev")
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = f"/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)

    if os.getenv("FIND_HISTORIC", True) in [True, "True", "true"]:
        watcher = CSVWatcher(csv_directory_path=CSV_DIRECTORY_PATH, client=DB_CLIENT)
        watcher.start()

    # api.register_blueprint(send_msgs_blueprint)
    # api.register_blueprint(acqs_blueprint)
    # api.register_blueprint(prtyps_blueprint)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)