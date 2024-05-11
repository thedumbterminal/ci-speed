from flask_restx import Resource, Namespace
from db.models import TestCase
from schemas import TestCaseSchema
from flask_security import auth_required


api = Namespace("slow test_cases", description="Slow test case related operations")

search_parser = api.parser()
search_parser.add_argument(
    "build_id", type=int, location="args", help="Build ID", required=True
)

@api.route("/")
class SlowTestCaseList(Resource):
    @api.expect(search_parser)
    @auth_required("token", "session")
    @api.doc(id="slow_test_cases", security=["apikey"])
    def get(self):
        """Retrieve the slowest test cases for a build"""
        args = search_parser.parse_args()
        test_cases = []
        test_case_schema = TestCaseSchema()
        return test_case_schema.dump(test_cases, many=True)
