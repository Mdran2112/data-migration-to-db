import json
import logging
import time
from flask_smorest import abort

from flask.views import MethodView
from flask_api.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_smorest import Blueprint

from api import RESTORE_SERVICE
from api.controllers import admin_auth
from database.models import EMPLOYEES_TABLE, DEPARTMENT_TABLE, JOB_TABLE

blp = Blueprint("Restore", "restore", description="Restore table from avro backup file.")

TABLES = [EMPLOYEES_TABLE, DEPARTMENT_TABLE, JOB_TABLE]


@blp.route("/restore/<string:table>")
class RestoreController(MethodView):

    @admin_auth.login_required
    @blp.response(HTTP_200_OK,
                  description="Table created from avro backup file.",
                  example={
                      "message": "Table restored from avro backup file.",
                      "code": HTTP_200_OK,
                      "status": "Created"
                  })
    def put(self, table: str):
        t0 = time.time()
        logging.info(f"Restoring table {table}...")
        if table not in TABLES:
            abort(HTTP_400_BAD_REQUEST, message=f"Please write an existing table: {TABLES}")
        res = RESTORE_SERVICE.restore(table=table)

        tf = time.time()

        total_time = tf - t0

        logging.info(f"Finished! Time: {round(total_time, 2)} secs.")
        logging.info(f"{json.dumps(res, indent=4)}")

        return res, res.get("code")
