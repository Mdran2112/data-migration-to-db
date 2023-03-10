from marshmallow import Schema, fields, validate
from marshmallow.validate import Length


class DepartmentSchema(Schema):
    id = fields.Int(required=True)
    department = fields.Str(required=True)


class DepartmentsBodySchema(Schema):
    departments = fields.List(fields.Nested(DepartmentSchema()), required=True, validate=Length(1, 1000))
