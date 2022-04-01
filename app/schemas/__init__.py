from flask_marshmallow import Marshmallow
from models import TestRun, TestSuite, TestCase

ma = Marshmallow()


class TestRunSchema(ma.SQLAlchemyAutoSchema):
    test_suites = ma.auto_field()

    class Meta:
        model = TestRun
        load_instance = True
        include_fk = True


class TestSuiteSchema(ma.SQLAlchemyAutoSchema):
    test_cases = ma.auto_field()

    class Meta:
        model = TestSuite
        load_instance = True
        include_fk = True


class TestCaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestCase
        load_instance = True
        include_fk = True
