from marshmallow import Schema, fields
from marshmallow.validate import Length


class JobSchema(Schema):
    id = fields.Int(missing=None)
    job = fields.Str(missing=None)


class JobsBodySchema(Schema):
    jobs = fields.List(fields.Nested(JobSchema()), required=True, validate=Length(1, 1000))
