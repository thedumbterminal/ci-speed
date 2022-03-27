from marshmallow import Schema, fields, RAISE
from .TestSuite import TestSuiteSchema


class TestRunSchema(Schema):
    created_at = fields.DateTime()
    test_suites = fields.List(fields.Nested(TestSuiteSchema))

    class Meta:
        unknown = RAISE
