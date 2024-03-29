from flask_restx import Resource, Namespace
from db.models import TestCase
from schemas import TestCaseSchema
from flask_security import auth_required


api = Namespace("test_cases", description="Test case related operations")

search_parser = api.parser()
search_parser.add_argument(
    "test_suite_id", type=int, location="args", help="Test suite ID", required=True
)


@api.route("/")
class TestCaseList(Resource):
    @api.expect(search_parser)
    @auth_required("token", "session")
    @api.doc(id="list_test_cases", security=["apikey"])
    def get(self):
        """List all test cases"""
        args = search_parser.parse_args()
        test_cases = TestCase.query.filter_by(test_suite_id=args["test_suite_id"]).all()
        test_case_schema = TestCaseSchema()
        return test_case_schema.dump(test_cases, many=True)
