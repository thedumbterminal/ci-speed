from flask_restx import Resource, Namespace
from flask_security import auth_required
from lib.repo import repo_list


api = Namespace(
    "available_projects", description="Available project related operations"
)


@api.route("/")
class AvailableProjectList(Resource):
    @auth_required("token", "session")
    @api.doc(id="list_available_projects", security=["apikey"])
    def get(self):
        """List all available projects"""

        return repo_list()
