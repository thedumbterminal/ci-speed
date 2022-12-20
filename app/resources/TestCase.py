from flask_restx import Resource, Namespace
from db.models import TestCase as TestCaseModel
from schemas import TestCaseSchema
from flask_security import auth_required


api = Namespace("test_cases", description="Test case related operations")


@api.route("/<int:case_id>")
@api.param("case_id", "The test case identifier")
class TestCase(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_test_case", security=["apikey"])
    def get(self, case_id):
        """Retrieve a test case"""
        test_case = TestCaseModel.query.get(case_id)
        test_case_schema = TestCaseSchema()
        return test_case_schema.dump(test_case)
