from marshmallow import Schema, fields, RAISE


class TestCaseSchema(Schema):
    name = fields.String()

    class Meta:
        unknown = RAISE
