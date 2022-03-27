from flask_restx import Resource, Namespace

api = Namespace("test_case", description="Test case related operations")


@api.route("/")
class TestCase(Resource):
    @api.doc("get_test_case")
    def get(self):
        return {'hello': 'world'}
