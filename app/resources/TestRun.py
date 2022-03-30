from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage
import xmltodict
from models import (TestRun as TestRunModel,
                    TestSuite as TestSuiteModel,
                    TestCase as TestCaseModel)
from schemas import TestRunSchema
from pprint import pprint
import json
from db import db

api = Namespace("test_run", description="Test run related operations")

upload_parser = api.parser()
upload_parser.add_argument(
    'file',
    location='files',
    type=FileStorage,
    required=True
)


@api.route("/")
class TestRun(Resource):
    def _jUnitToTestRun(self, junit_dict):
        test_suites = []
        for suite in junit_dict['testsuites']:
            suite_details = suite['testsuite']
            test_cases = []
            for case in suite_details['testcase']:
                test_case = TestCaseModel(case['@name'])
                test_cases.append(test_case)
            test_suite = TestSuiteModel(suite_details['@name'], test_cases)
            test_suites.append(test_suite)
        return TestRunModel(test_suites)

    @api.doc("get_test_run")
    def get(self):
        return {'hello': 'world'}

    @api.doc("post_test_run")
    @api.expect(upload_parser)
    def post(self):
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
