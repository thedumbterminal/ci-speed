from flask_marshmallow import Marshmallow
from models import TestRun, TestSuite, TestCase

ma = Marshmallow()


class TestRunSchema(ma.SQLAlchemyAutoSchema):
    test_suites = ma.auto_field()

    class Meta:
        model = TestRun
        include_fk = True


class TestSuiteSchema(ma.SQLAlchemyAutoSchema):
    test_cases = ma.auto_field()

    class Meta:
        model = TestSuite
        include_fk = True


class TestCaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestCase
        include_fk = True
