from flask_marshmallow import Marshmallow
from models import Project, TestRun, TestSuite, TestCase, User
from flask_marshmallow.fields import fields

ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    test_runs = ma.auto_field()

    class Meta:
        model = Project
        load_instance = True
        include_fk = True


class TestRunSchema(ma.SQLAlchemyAutoSchema):
    test_suites = ma.auto_field()

    class Meta:
        model = TestRun
        load_instance = True
        include_fk = True


class TestSuiteSchema(ma.SQLAlchemyAutoSchema):
    test_cases = ma.auto_field()
    time = fields.Float() # Allow numeric fields to be serialised correctly

    class Meta:
        model = TestSuite
        load_instance = True
        include_fk = True


class TestCaseSchema(ma.SQLAlchemyAutoSchema):
    time = fields.Float() # Allow numeric fields to be serialised correctly

    class Meta:
        model = TestCase
        load_instance = True
        include_fk = True
