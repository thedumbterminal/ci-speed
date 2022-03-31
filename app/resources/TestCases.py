from flask_restx import Resource, Namespace

api = Namespace("test_cases", description="Test case related operations")


@api.route("/")
class TestCases(Resource):
    @api.doc("get_test_case")
    def get(self):
        return {'hello': 'world'}
