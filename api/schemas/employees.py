from marshmallow import Schema, fields
from marshmallow.validate import Length


class EmployeeSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str(missing=None)
    datetime = fields.DateTime(missing=None)
    department_id = fields.Int(missing=None)
    job_id = fields.Int(missing=None)


class EmployeesBodySchema(Schema):

    employees = fields.List(fields.Nested(EmployeeSchema()), required=True, validate=Length(1, 1000))
