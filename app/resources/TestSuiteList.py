from flask_restx import Resource, Namespace
from models import TestSuite
from schemas import TestSuiteSchema

api = Namespace("test_suites", description="Test suite related operations")


@api.route("/")
class TestSuiteList(Resource):
    @api.doc("list_test_suites")
    def get(self):
        '''List all test suites'''
        test_suites = TestSuite.query.all()
        test_suite_schema = TestSuiteSchema()
        return test_suite_schema.dump(test_suites, many=True)

