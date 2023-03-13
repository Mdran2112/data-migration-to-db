import json
import logging
import time

from flask_api.status import HTTP_200_OK
from flask_smorest import Blueprint

from api.controllers import auth

blp = Blueprint("Restore", "restore", description="Restore table from avro backup file.")


@blp.route("/restore/<string:table>")
class RestoreController:

    @auth.login_required
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

        res = ...

        tf = time.time()

        total_time = tf - t0

        logging.info(f"Finished! Time: {round(total_time, 2)} secs.")
        logging.info(f"{json.dumps(res, indent=4)}")

        return res, res.get("code")
