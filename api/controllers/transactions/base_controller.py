import json
import logging
import time
from typing import Dict, Any

from flask.views import MethodView

from api import TRANSACTION_SERVICE


class BaseController(MethodView):

    table: str = ...

    def post(self, input_params: Dict[str, Any]):
        t0 = time.time()
        logging.info(f"Inserting data into {self.table} DB...")
        res = TRANSACTION_SERVICE.insert_to_db(table=self.table, objects=input_params[self.table])
        tf = time.time()

        total_time = tf - t0

        logging.info(f"Finished! Time: {round(total_time, 2)} secs.")
        logging.info(f"{json.dumps(res, indent=4)}")

        return res, res.get("code")