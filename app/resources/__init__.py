from flask_restx import Api

from .TestCases import api as test_case_api
from .TestRunList import api as test_run_list_api
from .TestRun import api as test_run_api
from .TestSuites import api as test_suite_api

api = Api(
    title="CI-Speed API",
    version="1.0",
    description="Manage CI-Speed resources"
)

api.add_namespace(test_case_api)
api.add_namespace(test_run_list_api)
api.add_namespace(test_run_api)
api.add_namespace(test_suite_api)
