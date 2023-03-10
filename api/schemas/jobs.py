from marshmallow import Schema, fields
from marshmallow.validate import Length


class JobSchema(Schema):
    id = fields.Int(required=True)
    job = fields.Str(required=True)


class JobsBodySchema(Schema):
    jobs = fields.List(fields.Nested(JobSchema()), required=True, validate=Length(1, 1000))
