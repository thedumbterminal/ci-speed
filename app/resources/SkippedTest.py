from flask_restx import Resource, Namespace
from models import SkippedTest as Model
from schemas import SkippedTestSchema as Schema
from flask_security import auth_required


api = Namespace("skipped_tests", description="Skipped test related operations")


@api.route("/<int:id>")
@api.param("id", "The skipped test identifier")
class SkippedTest(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_skipped_test", security=["apikey"])
    def get(self, id):
        """Retrieve a skipped test"""
        model = Model.query.get(id)
        schema = Schema()
        return schema.dump(model)
