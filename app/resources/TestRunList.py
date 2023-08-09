from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage
import xmltodict
from db.models import (
    Build,
    TestRun,
    TestSuite,
    TestCase,
    TestFailure,
    SkippedTest,
)
from schemas import TestRunSchema
from pprint import pprint
import json
from db.connection import db
import os
from flask_security import auth_required, current_user
from models.project import find_by_name


api = Namespace("test_runs", description="Test run related operations")

upload_parser = api.parser()
upload_parser.add_argument(
    "file", location="files", type=FileStorage, help="XML file", required=True
)
upload_parser.add_argument(
    "project_name", required=True, help="Name of the project", location="form"
)
upload_parser.add_argument(
    "build_ref", required=True, help="Reference of the build", location="form"
)
upload_parser.add_argument(
    "commit_sha", required=False, help="Commit SHA of the build", location="form"
)

search_parser = api.parser()
search_parser.add_argument(
    "build_id", type=int, location="args", help="Build ID", required=True
)


@api.route("/")
class TestRunList(Resource):
    def _junit_to_test_case(self, case_details):
        test_failures = []
        skipped_tests = []
        # having test failure is optional
        if "failure" in case_details:
            # some implementations state a failure message and a failure text
            if "#text" in case_details["failure"]:
                test_failure = TestFailure(case_details["failure"]["#text"])
            else:
                test_failure = TestFailure(case_details["failure"])
            test_failures.append(test_failure)
        # having a skipped test is optional
        if "skipped" in case_details:
            # some implementations state a skipped message and a failure text
            if "#text" in case_details["skipped"]:
                skipped_test = SkippedTest(case_details["skipped"]["#text"])
            else:
                skipped_test = SkippedTest(case_details["skipped"])
            skipped_tests.append(skipped_test)
        return TestCase(
            case_details["@name"], case_details["@time"], test_failures, skipped_tests
        )

    def _junit_to_test_suite(self, suite_details):
        print(suite_details["testcase"])
        test_cases = []
        for case in suite_details["testcase"]:
            test_case = self._junit_to_test_case(case)
            test_cases.append(test_case)
        return TestSuite(suite_details["@name"], suite_details["@time"], test_cases)

    def _junit_to_test_run(self, build_id, junit_dict):
        test_suites = []
        # having testsuites is optional
        if "testsuites" in junit_dict:
            for suite in junit_dict["testsuites"]:
                test_suite = self._junit_to_test_suite(suite["testsuite"])
                test_suites.append(test_suite)
        else:
            test_suite = self._junit_to_test_suite(junit_dict["testsuite"])
            test_suites.append(test_suite)
        return TestRun(build_id, test_suites)

    def _test_run_url(self, test_run):
        server_url_base = os.environ.get("SERVER_URL_BASE", "http://localhost:5000")
        return f"{server_url_base}/#/test_run/?id={test_run.id}"

    @api.expect(search_parser)
    @auth_required("token", "session")
    @api.doc(id="list_test_runs", security=["apikey"])
    def get(self):
        """List all test runs"""
        args = search_parser.parse_args()
        test_runs = TestRun.query.filter_by(build_id=args["build_id"]).all()
        test_run_schema = TestRunSchema()
        return test_run_schema.dump(test_runs, many=True)

    @api.expect(upload_parser)
    @auth_required("token", "session")
    @api.doc(id="upload_test_run", security=["apikey"])
    def post(self):
        """Upload a junit XML file to create a test run"""
        args = upload_parser.parse_args()
        uploaded_file = args["file"]  # This is FileStorage instance
        converted_dict = xmltodict.parse(
            uploaded_file.read(), force_list=("testsuites", "testsuite", "testcase")
        )
        print("Uploaded dict:")
        pprint(converted_dict)
        print("Uploaded JSON:")
        print(json.dumps(converted_dict))

        project = find_by_name(current_user, args["project_name"])
        if not project:
            raise ValueError("Project not found")
        print("Found project", project)
        build = Build.query.filter_by(ref=args["build_ref"]).first()
        if not build:
            build = Build(project.id, args["build_ref"], args["commit_sha"])
            db.session.add(build)
            db.session.commit()
        print("Found build", build)
        test_run = self._junit_to_test_run(build.id, converted_dict)
        db.session.add(test_run)
        db.session.commit()

        return {"test_run_url": self._test_run_url(test_run)}
