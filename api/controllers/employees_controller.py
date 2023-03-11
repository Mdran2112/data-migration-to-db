from typing import Dict, Any

from flask_api.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from flask_smorest import Blueprint

from api.controllers import auth
from api.controllers.base_controller import BaseController
from api.schemas import EmployeesBodySchema
from database.models import EMPLOYEES_TABLE
from globals import HTTP_422_UNPROCESSABLE_ENTITY

blp = Blueprint("Employees", "employees", description="")


@blp.route("/employees")
class EmployeesController(BaseController):
    table: str = EMPLOYEES_TABLE

    @auth.login_required
    @blp.arguments(EmployeesBodySchema,
                   example={
                       "employees": [
                           {
                               "id": 2006, "name": "Martin", "datetime": "2023-03-10T02:48:42",
                               "department_id": 4, "job_id": 71
                           },
                           {
                               "id": 2006, "name": "Liz", "datetime": "2023-03-10T02:48:42",
                               "department_id": 4, "job_id": 72
                           }
                       ]
                   })
    @blp.response(HTTP_201_CREATED,
                  description="Inserts employees data in database.",
                  example={
                      "message": f"Data inserted in {table} table",
                      "code": HTTP_201_CREATED,
                      "status": "Created"
                  })
    @blp.response(HTTP_422_UNPROCESSABLE_ENTITY,
                  description=".",
                  example={
                      "code": 422,
                      "message": [
                          "None of the objects could be inserted, maybe because all of them didn't satisfied the Data "
                          "Rules."
                      ],
                      "status": "Unprocessable Entity"
                  })
    def post(self, input_params: Dict[str, Any]):
        return super().post(input_params)
