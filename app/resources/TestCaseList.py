from flask_restx import Resource, Namespace
from models import TestCase
from schemas import TestCaseSchema

api = Namespace("test_cases", description="Test case related operations")

search_parser = api.parser()
search_parser.add_argument(
    'test_suite_id',
    type=int,
    location='args',
    help='Test suite ID',
    required=True
)

@api.route("/")
class TestCaseList(Resource):
    @api.doc("list_test_cases")
    @api.expect(search_parser)
    def get(self):
        '''List all test cases'''
        args = search_parser.parse_args()
        test_cases = TestCase.query.filter_by(test_suite_id = args['test_suite']).all()
        test_case_schema = TestCaseSchema()
        return test_case_schema.dump(test_cases, many=True)
