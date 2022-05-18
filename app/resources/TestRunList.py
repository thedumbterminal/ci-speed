from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage
import xmltodict
from models import Project, Build, TestRun, TestSuite, TestCase
from schemas import TestRunSchema
from pprint import pprint
import json
from db import db
import os
from flask_security import auth_required, current_user


api = Namespace("test_runs", description="Test run related operations")

upload_parser = api.parser()
upload_parser.add_argument(
    'file',
    location='files',
    type=FileStorage,
    help='XML file',
    required=True
)
upload_parser.add_argument(
    'project_name',
    required=True,
    help='Name of the project',
    location='form'
)
upload_parser.add_argument(
    'build_ref',
    required=True,
    help='Reference of the build',
    location='form'
)

search_parser = api.parser()
search_parser.add_argument(
    'project_id',
    type=int,
    location='args',
    help='Project ID',
    required=True
)

@api.route("/")
class TestRunList(Resource):
    def _junit_to_test_suite(self, suite_details):
        test_cases = []
        for case in suite_details['testcase']:
            test_case = TestCase(case['@name'], case['@time'])
            test_cases.append(test_case)
        return TestSuite(suite_details['@name'], suite_details['@time'], test_cases)

    def _junit_to_test_run(self, build_id, junit_dict):
        test_suites = []
        # having testsuites is optional
        if 'testsuites' in junit_dict:
            for suite in junit_dict['testsuites']:
                test_suite = self._junit_to_test_suite(suite['testsuite'])
                test_suites.append(test_suite)
        else:
            test_suite = self._junit_to_test_suite(junit_dict['testsuite'])
            test_suites.append(test_suite)
        return TestRun(build_id, test_suites)

    def _test_run_url(self, test_run):
        ui_url_base = os.environ.get('UI_URL_BASE', 'http://localhost:5000')
        ui_url_path = os.environ.get('UI_URL_PATH', '/')
        return f'{ui_url_base}{ui_url_path}#/test_run/?id={test_run.id}'

    @api.doc("list_test_runs")
    @api.expect(search_parser)
    @auth_required('token', 'session')
    @api.doc(security=['apikey'])
    def get(self):
        '''List all test runs'''
        args = search_parser.parse_args()
        test_runs = TestRun.query.filter_by(project_id = args['project_id']).all()
        test_run_schema = TestRunSchema()
        return test_run_schema.dump(test_runs, many=True)

    @api.doc("upload_test_run")
    @api.expect(upload_parser)
    @auth_required('token', 'session')
    @api.doc(security=['apikey'])
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

        project = Project.query.filter_by(name = args['project_name']).first()
        if not project:
            raise ValueError('Project not found')
        print('Found project', project)
        build = Build.query.filter_by(ref = args['build_ref']).first()
        if not build:
            build = Build(project.id, args['build_ref'])
            db.session.add(build)
        print('Found build', build)
        test_run = self._junit_to_test_run(build.id, converted_dict)
        db.session.add(test_run)
        db.session.commit()

        print('Schema result:')
        test_run_schema = TestRunSchema()
        pprint(test_run_schema.dump(test_run))
        return {
            'test_run_url': self._test_run_url(test_run)
        }
