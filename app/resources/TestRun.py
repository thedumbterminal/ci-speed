from flask_restx import Resource, Namespace
from models import TestRun as TestRunModel
from schemas import TestRunSchema
from flask_security import auth_required


api = Namespace("test_runs", description="Test run related operations")


@api.route("/<int:id>")
@api.param("id", "The test run identifier")
class TestRun(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_test_run", security=["apikey"])
    def get(self, test_run_id):
        """Retrieve a test run"""
        test_run = TestRunModel.query.get(test_run_id)
        test_run_schema = TestRunSchema()
        return test_run_schema.dump(test_run)
