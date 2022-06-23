from flask_marshmallow import Marshmallow
from models import User, Project, Build, TestRun, TestSuite, TestCase, TestFailure, SkippedTest
from flask_marshmallow.fields import fields

ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ("fs_uniquifier", "password", "confirmed_at")


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    builds = ma.auto_field()

    class Meta:
        model = Project
        load_instance = True
        include_fk = True


class BuildSchema(ma.SQLAlchemyAutoSchema):
    test_runs = ma.auto_field()

    class Meta:
        model = Build
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
    time = fields.Float()  # Allow numeric fields to be serialised correctly

    class Meta:
        model = TestSuite
        load_instance = True
        include_fk = True


class TestCaseSchema(ma.SQLAlchemyAutoSchema):
    test_failures = ma.auto_field()
    skipped_tests = ma.auto_field()
    time = fields.Float()  # Allow numeric fields to be serialised correctly

    class Meta:
        model = TestCase
        load_instance = True
        include_fk = True


class TestFailureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestFailure
        load_instance = True
        include_fk = True


class SkippedTestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SkippedTest
        load_instance = True
        include_fk = True
