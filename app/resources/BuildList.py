from flask_restx import Resource, Namespace
from db.models import Build
from schemas import BuildSchema
from pprint import pprint
from db.connection import db
from flask_security import auth_required, current_user
from models.project import find_by_name


api = Namespace("builds", description="Build related operations")

create_parser = api.parser()
create_parser.add_argument(
    "project_name", required=True, help="name of the project", location="form"
)
create_parser.add_argument(
    "ref", required=True, help="Reference for the build", location="form"
)
create_parser.add_argument(
    "commit_sha", required=False, help="Commit SHA of the build", location="form"
)

search_parser = api.parser()
search_parser.add_argument(
    "project_id", type=int, location="args", help="Project ID", required=True
)


@api.route("/")
class BuildList(Resource):
    @api.expect(search_parser)
    @auth_required("token", "session")
    @api.doc(id="list_builds", security=["apikey"])
    def get(self):
        """List all builds"""
        args = search_parser.parse_args()
        builds = Build.query.filter_by(project_id=args["project_id"]).all()
        build_schema = BuildSchema()
        return build_schema.dump(builds, many=True)

    @api.expect(create_parser)
    @auth_required("token", "session")
    @api.doc(id="create_build", security=["apikey"])
    def post(self):
        """Create a new build for storing test runs against"""
        args = create_parser.parse_args()
        project = find_by_name(current_user, args["project_name"])
        if not project:
            raise ValueError("Project not found")
        print("Found project", project)
        build = Build(project.id, args["ref"], args["commit_sha"])
        db.session.add(build)
        db.session.commit()

        print("Schema result:")
        build_schema = BuildSchema()
        pprint(build_schema.dump(build))
        return True
