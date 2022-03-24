from flask_restx import Api

from .TestResult import api as test_result_api

api = Api(title="CI-Speed API", version="1.0", description="Manage CI-Speed resources")

api.add_namespace(test_result_api)