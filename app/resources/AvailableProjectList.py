from flask_restx import Resource, Namespace
from lib.repo import repo_list
from flask_security import auth_required, current_user

api = Namespace(
    "available_projects", description="Available project related operations"
)


@api.route("/")
class AvailableProjectList(Resource):
    @auth_required("token", "session")
    @api.doc(id="list_available_projects", security=["apikey"])
    def get(self):
        """List all available projects"""

        current_projects = current_user.projects
        current_project_names = list(map(lambda x: x.name, current_projects))

        repos = repo_list()

        # exclude projects that have already been setup
        available = list(filter(lambda x: x not in current_project_names, repos))
        return available
