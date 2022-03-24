from flask_restx import Resource, Namespace

api = Namespace("test_results", description="Test results related operations")

@api.route("/")
class TestResult(Resource):
    @api.doc("get_test_result")
    def get(self):
        return {'hello': 'world'}
