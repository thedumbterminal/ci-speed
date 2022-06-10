from flask_restx import Resource, Namespace
from models import TestFailure
from schemas import TestFailureSchema
from flask_security import auth_required


api = Namespace("test_failures", description="Test failure related operations")

search_parser = api.parser()
search_parser.add_argument(
    "test_case_id", type=int, location="args", help="Test case ID", required=True
)


@api.route("/")
class TestFailureList(Resource):
    @api.doc("list_test_failures")
    @api.expect(search_parser)
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self):
        """List all test failures"""
        args = search_parser.parse_args()
        test_failures = TestFailure.query.filter_by(
            test_suite_id=args["test_case_id"]
        ).all()
        test_failure_schema = TestFailureSchema()
        return test_failure_schema.dump(test_failures, many=True)
