from flask_restx import Resource, Namespace
from models import TestFailure as TestFailureModel
from schemas import TestFailureSchema
from flask_security import auth_required


api = Namespace("test_failures", description="Test failure related operations")


@api.route("/<int:id>")
@api.param("id", "The test failure identifier")
class TestFailure(Resource):
    @api.doc("get_test_failure")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, id):
        """Retrieve a test failure"""
        test_failure = TestFailureModel.query.get(id)
        test_failure_schema = TestFailureSchema()
        return test_failure_schema.dump(test_failure)
