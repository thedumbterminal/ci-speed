from flask_restx import Api

from .TestCase import api as test_case_api
from .TestRun import api as test_run_api
from .TestSuite import api as test_suite_api

api = Api(title="CI-Speed API", version="1.0", description="Manage CI-Speed resources")

api.add_namespace(test_case_api)
api.add_namespace(test_run_api)
api.add_namespace(test_suite_api)
