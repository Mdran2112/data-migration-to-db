from typing import Dict, Any

from flask_api.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from flask_smorest import Blueprint

from api.controllers import auth
from api.controllers.base_controller import BaseController
from api.schemas import JobsBodySchema
from database.models import JOB_TABLE
from globals import HTTP_422_UNPROCESSABLE_ENTITY

blp = Blueprint("Jobs", "jobs", description="")


@blp.route("/jobs")
class DepartmentsController(BaseController):

    table: str = JOB_TABLE

    @auth.login_required
    @blp.arguments(JobsBodySchema,
                   example={
                       "jobs": [
                           {
                               "id": 1,
                               "job": "Manager"
                           },
                           {
                               "id": 2,
                               "job": "Recruiter"
                           }
                       ]
                   })
    @blp.response(HTTP_201_CREATED,
                  description="Inserts jobs data in database.",
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
