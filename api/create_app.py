import os
import time

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from api import DB_CLIENT, AllFieldsRequired, BACKUP_CLIENT
from api.workers.backup_worker import BackupWorker
from api.workers.csv_watcher_worker import CSVWatcherWorker
from globals import CSV_DIRECTORY_PATH

from api.controllers.employees_controller import blp as employees_blp
from api.controllers.departments_controller import blp as departments_blp
from api.controllers.jobs_controllers import blp as jobs_blp


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

    api.register_blueprint(employees_blp)
    api.register_blueprint(departments_blp)
    api.register_blueprint(jobs_blp)

    return app


if __name__ == "__main__":

    if os.getenv("FIND_HISTORIC", True) in [True, "True", "true"]:
        watcher = CSVWatcherWorker(csv_directory_path=CSV_DIRECTORY_PATH, client=DB_CLIENT, rules=[AllFieldsRequired()])
        historic_csv_sched = BackgroundScheduler()
        historic_csv_sched.add_job(watcher.run, 'interval', seconds=5)
        historic_csv_sched.start()

    time.sleep(5)

    if os.getenv("BUILD_BACKUP", True) in [True, "True", "true"]:
        backup_worker = BackupWorker(client=BACKUP_CLIENT)
        backup_sched = BackgroundScheduler()
        backup_sched.add_job(backup_worker.run, 'interval', seconds=5)
        backup_sched.start()

    create_app().run(debug=True)
