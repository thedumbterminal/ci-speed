from marshmallow import Schema, fields, RAISE
from .TestCase import TestCaseSchema


class TestSuiteSchema(Schema):
    name = fields.String()
    test_cases = fields.List(fields.Nested(TestCaseSchema))

    class Meta:
        unknown = RAISE
