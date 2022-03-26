from flask_restx import Resource, Namespace

api = Namespace("test_suite", description="Test suite related operations")

@api.route("/")
class TestSuite(Resource):
    @api.doc("get_test_suite")
    def get(self):
        return {'hello': 'world'}
