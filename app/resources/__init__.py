from flask_restx import Api

from .ProjectList import api as project_list_api
from .Project import api as project_api
from .TestRunList import api as test_run_list_api
from .TestRun import api as test_run_api
from .TestSuite import api as test_suite_api
from .TestSuiteList import api as test_suite_list_api
from .TestCase import api as test_case_api
from .TestCaseList import api as test_case_list_api
from .Auth import api as auth_api

api = Api(
    title="CI-Speed API",
    version="1.0",
    description="Manage CI-Speed resources"
)

api.add_namespace(project_list_api)
api.add_namespace(project_api)
api.add_namespace(test_run_list_api)
api.add_namespace(test_run_api)
api.add_namespace(test_suite_api)
api.add_namespace(test_suite_list_api)
api.add_namespace(test_case_api)
api.add_namespace(test_case_list_api)
api.add_namespace(auth_api)
