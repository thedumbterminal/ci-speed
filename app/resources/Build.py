from flask_restx import Resource, Namespace
from models import Build as BuildModel
from schemas import BuildSchema
from flask_security import auth_required


api = Namespace("builds", description="Build related operations")


@api.route("/<int:id>")
@api.param("id", "The build identifier")
class Build(Resource):
    @api.doc("get_build")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, id):
        """Retrieve a build"""
        build = BuildModel.query.get(id)
        build_schema = BuildSchema()
        return build_schema.dump(build)
