from flask_restx import Resource, Namespace
from db.models import TestSuite as TestSuiteModel
from schemas import TestSuiteSchema
from flask_security import auth_required

api = Namespace("test_suites", description="Test suite related operations")


@api.route("/<int:suite_id>")
@api.param("suite_id", "The test suite identifier")
class TestSuite(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_test_suite", security=["apikey"])
    def get(self, suite_id):
        """Retrieve a test suite"""
        test_suite = TestSuiteModel.query.get(suite_id)
        test_suite_schema = TestSuiteSchema()
        return test_suite_schema.dump(test_suite)
