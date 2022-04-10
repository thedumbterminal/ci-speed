from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage
import xmltodict
from models import TestRun, TestSuite, TestCase
from schemas import TestRunSchema
from pprint import pprint
import json
from db import db

api = Namespace("test_runs", description="Test run related operations")

upload_parser = api.parser()
upload_parser.add_argument(
    'file',
    location='files',
    type=FileStorage,
    help='XML file',
    required=True
)


@api.route("/")
class TestRunList(Resource):
    def _jUnitToTestRun(self, junit_dict):
        test_suites = []
        for suite in junit_dict['testsuites']:
            suite_details = suite['testsuite']
            test_cases = []
            for case in suite_details['testcase']:
                test_case = TestCase(case['@name'])
                test_cases.append(test_case)
            test_suite = TestSuite(suite_details['@name'], test_cases)
            test_suites.append(test_suite)
        return TestRun(test_suites)

    @api.doc("list_test_runs")
    def get(self):
        '''List all test runs'''
        test_runs = TestRun.query.all()
        test_run_schema = TestRunSchema()
        return test_run_schema.dump(test_runs, many=True)

    @api.doc("upload_test_run")
    @api.expect(upload_parser)
    def post(self):
        '''Upload a junit XML file to create a test run'''
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        converted_dict = xmltodict.parse(
            uploaded_file.read(),
            force_list=('testsuites', 'testcase')
        )
        print('Uploaded dict:')
        pprint(converted_dict)
        print('Uploaded JSON:')
        print(json.dumps(converted_dict))

        test_run = self._jUnitToTestRun(converted_dict)
        db.session.add(test_run)
        db.session.commit()

        print('Schema result:')
        test_run_schema = TestRunSchema()
        pprint(test_run_schema.dump(test_run))
        return True
