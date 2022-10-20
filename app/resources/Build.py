from flask_restx import Resource, Namespace
from models import Build as BuildModel
from schemas import BuildSchema
from flask_security import auth_required


api = Namespace("builds", description="Build related operations")


@api.route("/<int:build_id>")
@api.param("build_id", "The build identifier")
class Build(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_build", security=["apikey"])
    def get(self, build_id):
        """Retrieve a build"""
        build = BuildModel.query.get(build_id)
        build_schema = BuildSchema()
        return build_schema.dump(build)
