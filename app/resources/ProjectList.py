from flask_restx import Resource, Namespace
from db.models import Project
from schemas import ProjectSchema
from db.connection import db
from flask_security import auth_required, current_user
from lib.repo import repo_list
from sqlalchemy.orm.exc import NoResultFound


api = Namespace("projects", description="Project related operations")

create_parser = api.parser()
create_parser.add_argument(
    "name", required=True, help="Name of the project", location="form"
)


@api.route("/")
class ProjectList(Resource):
    @auth_required("token", "session")
    @api.doc(id="list_projects", security=["apikey"])
    def get(self):
        """List all projects"""
        project_schema = ProjectSchema()
        return project_schema.dump(current_user.projects, many=True)

    @api.expect(create_parser)
    @auth_required("token", "session")
    @api.doc(id="create_project", security=["apikey"])
    def post(self):
        """Create a new project for storing builds against"""
        args = create_parser.parse_args()

        repos = repo_list()

        # Check if the project provided is one of the user's repos
        if args["name"] not in repos:
            raise "Invalid project name"

        # Dont create the project if it already exists
        query = Project.query.filter_by(name=args["name"])
        try:
            project = query.one()
        except NoResultFound:
            project = Project(args["name"])
        current_user.projects.append(project)
        db.session.add(current_user)
        db.session.commit()

        return True
