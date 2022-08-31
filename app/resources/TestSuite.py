from flask_restx import Resource, Namespace
from models import TestSuite as TestSuiteModel
from schemas import TestSuiteSchema
from flask_security import auth_required

api = Namespace("test_suites", description="Test suite related operations")


@api.route("/<int:id>")
@api.param("id", "The test suite identifier")
class TestSuite(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_test_suite", security=["apikey"])
    def get(self, id):
        """Retrieve a test suite"""
        test_suite = TestSuiteModel.query.get(id)
        test_suite_schema = TestSuiteSchema()
        return test_suite_schema.dump(test_suite)
