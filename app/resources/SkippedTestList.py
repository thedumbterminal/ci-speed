from flask_restx import Resource, Namespace
from db.models import TestFailure as Model
from schemas import TestFailureSchema as Schema
from flask_security import auth_required


api = Namespace("skipped_tests", description="Skipped tests related operations")

search_parser = api.parser()
search_parser.add_argument(
    "test_case_id", type=int, location="args", help="Test case ID", required=True
)


@api.route("/")
class SkippedTestsList(Resource):
    @api.expect(search_parser)
    @auth_required("token", "session")
    @api.doc(id="list_skipped_tests", security=["apikey"])
    def get(self):
        """List all skipped tests"""
        args = search_parser.parse_args()
        models = Model.query.filter_by(test_suite_id=args["test_case_id"]).all()
        schema = Schema()
        return schema.dump(models, many=True)
