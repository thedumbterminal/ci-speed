from flask_restx import Api

from .AvailableProjectList import api as available_project_list_api
from .ProjectList import api as project_list_api
from .Project import api as project_api
from .BuildList import api as build_list_api
from .Build import api as build_api
from .TestRunList import api as test_run_list_api
from .TestRun import api as test_run_api
from .TestSuite import api as test_suite_api
from .TestSuiteList import api as test_suite_list_api
from .TestCase import api as test_case_api
from .TestCaseList import api as test_case_list_api
from .TestFailure import api as test_failure_api
from .TestFailureList import api as test_failure_list_api
from .SkippedTest import api as skipped_test_api
from .SkippedTestList import api as skipped_test_list_api
from .SlowTestCaseList import api as slow_test_case_list_api
from .Login import api as login_api
from .User import api as user_api
from .Token import api as token_api

authorizations = {
    # 'OAuth2': {
    # 'type': 'oauth2',
    # 'flow': 'accessCode',
    # 'authorizationUrl': 'https://github.com/login/oauth/authorize',
    # 'tokenUrl': '/oauth/github/authorized',
    # 'scopes': {
    # 'user:email': 'Read user email addresses'
    # }
    # },
    "apikey": {"type": "apiKey", "in": "header", "name": "Authentication-Token"}
}

api = Api(
    title="CI-Speed API",
    version="1.0.0",
    description="Manage CI-Speed resources",
    authorizations=authorizations,
    doc="/doc",
    prefix="/api",
)

api.add_namespace(available_project_list_api)
api.add_namespace(project_list_api)
api.add_namespace(project_api)
api.add_namespace(build_list_api)
api.add_namespace(build_api)
api.add_namespace(test_run_list_api)
api.add_namespace(test_run_api)
api.add_namespace(test_suite_api)
api.add_namespace(test_suite_list_api)
api.add_namespace(test_case_api)
api.add_namespace(test_case_list_api)
api.add_namespace(test_failure_api)
api.add_namespace(test_failure_list_api)
api.add_namespace(skipped_test_api)
api.add_namespace(skipped_test_list_api)
api.add_namespace(slow_test_case_list_api)
api.add_namespace(login_api)
api.add_namespace(user_api)
api.add_namespace(token_api)
