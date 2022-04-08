from flask_restx import Resource, Namespace
from models import TestSuite
from schemas import TestSuiteSchema

api = Namespace("test_suites", description="Test suite related operations")

search_parser = api.parser()
search_parser.add_argument(
    'test_run',
    type=int,
    location='args',
    help='Test run ID',
    required=True
)

@api.route("/")
class TestSuiteList(Resource):
    @api.doc("list_test_suites")
    @api.expect(search_parser)
    def get(self):
        '''List all test suites'''
        args = search_parser.parse_args()
        test_suites = TestSuite.query.filter_by(test_run_id = args['test_run']).all()
        test_suite_schema = TestSuiteSchema()
        return test_suite_schema.dump(test_suites, many=True)

