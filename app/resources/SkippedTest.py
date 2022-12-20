from flask_restx import Resource, Namespace
from db.models import SkippedTest as Model
from schemas import SkippedTestSchema as Schema
from flask_security import auth_required


api = Namespace("skipped_tests", description="Skipped test related operations")


@api.route("/<int:skipped_id>")
@api.param("skipped_id", "The skipped test identifier")
class SkippedTest(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_skipped_test", security=["apikey"])
    def get(self, skipped_id):
        """Retrieve a skipped test"""
        model = Model.query.get(skipped_id)
        schema = Schema()
        return schema.dump(model)
