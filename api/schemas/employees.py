from marshmallow import Schema, fields
from marshmallow.validate import Length


class EmployeeSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    datetime = fields.DateTime(required=True)
    department_id = fields.Int(required=True)
    job_id = fields.Int(required=True)


class EmployeesBodySchema(Schema):

    employees = fields.List(fields.Nested(EmployeeSchema()), required=True, validate=Length(1, 1000))
