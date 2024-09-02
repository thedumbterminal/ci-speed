from flask_restx import Resource, Namespace
from db.models import Waypoint, Build
from schemas import WaypointSchema as Schema
from flask_security import auth_required, current_user
from models.project import find_by_name
from db.connection import db
from pprint import pprint


api = Namespace("waypoints", description="Waypoint related operations")

create_parser = api.parser()
create_parser.add_argument(
    "waypoint", required=True, help="Name of the waypoint", location="form"
)
create_parser.add_argument(
    "project_name", required=True, help="Name of the project", location="form"
)
create_parser.add_argument(
    "build_ref", required=True, help="Reference of the build", location="form"
)
create_parser.add_argument(
    "commit_sha", required=False, help="Commit SHA of the build", location="form"
)

search_parser = api.parser()
search_parser.add_argument(
    "build_id", type=int, location="args", help="Build ID", required=True
)


@api.route("/")
class WaypointList(Resource):
    @auth_required("token", "session")
    @api.doc("list_waypoints")
    @api.expect(search_parser)
    @api.doc(security=["apikey"])
    def get(self):
        """List all waypoints"""
        args = search_parser.parse_args()
        results = Waypoint.query.filter_by(build_id=args["build_id"]).all()
        model_schema = Schema()
        return model_schema.dump(results, many=True)

    @api.expect(create_parser)
    @auth_required("token", "session")
    @api.doc(id="create_waypoint", security=["apikey"])
    def post(self):
        """Create a new waypoint"""
        args = create_parser.parse_args()
        project = find_by_name(current_user, args["project_name"])
        if not project:
            raise ValueError("Project not found")
        print("Found project", project)
        build = Build.query.filter_by(ref=args["build_ref"]).first()
        if not build:
            build = Build(project.id, args["build_ref"], args["commit_sha"])
            db.session.add(build)
            db.session.commit()
        print("Found build", build)

        waypoint = Waypoint(build.id, args["waypoint"])
        db.session.add(waypoint)
        db.session.commit()

        print("Schema result:")
        model_schema = Schema()
        pprint(model_schema.dump(waypoint))
        return True
