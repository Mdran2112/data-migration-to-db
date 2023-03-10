from typing import Dict, Any

from flask_api.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from flask_smorest import Blueprint

from api.controllers import auth
from api.controllers.base_controller import BaseController
from api.schemas import DepartmentsBodySchema
from database.models import DEPARTMENT_TABLE

blp = Blueprint("Departments", "departments", description="")


@blp.route("/departments")
class DepartmentsController(BaseController):

    table: str = DEPARTMENT_TABLE

    @auth.login_required
    @blp.arguments(DepartmentsBodySchema,
                   example={
                       "departments": []
                   })
    @blp.response(HTTP_201_CREATED,
                  description="Inserts departments data in database.",
                  example={
                      "message": f"Data inserted in {table} table",
                      "code": HTTP_201_CREATED,
                      "status": "Created"
                  })
    @blp.response(HTTP_400_BAD_REQUEST,
                  description=".",
                  example={})
    def post(self, input_params: Dict[str, Any]):
        return super().post(input_params)

