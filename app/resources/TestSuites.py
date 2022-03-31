from flask_restx import Resource, Namespace

api = Namespace("test_suites", description="Test suite related operations")


@api.route("/")
class TestSuites(Resource):
    @api.doc("get_test_suite")
    def get(self):
        return {'hello': 'world'}
