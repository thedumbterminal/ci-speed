from flask_restx import Resource, Namespace
from db.models import TestSuite
from schemas import TestSuiteSchema
from flask_security import auth_required

api = Namespace("test_suites", description="Test suite related operations")

search_parser = api.parser()
search_parser.add_argument(
    "test_run_id", type=int, location="args", help="Test run ID", required=True
)


@api.route("/")
class TestSuiteList(Resource):
    @auth_required("token", "session")
    @api.doc("list_test_suites")
    @api.expect(search_parser)
    @api.doc(security=["apikey"])
    def get(self):
        """List all test suites"""
        args = search_parser.parse_args()
        test_suites = TestSuite.query.filter_by(test_run_id=args["test_run_id"]).all()
        test_suite_schema = TestSuiteSchema()
        return test_suite_schema.dump(test_suites, many=True)
