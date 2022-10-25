from flask_restx import Resource, Namespace
from flask_security import auth_required
from flask_dance.contrib.github import github

api = Namespace(
    "available_projects", description="Available project related operations"
)


@api.route("/")
class AvailableProjectList(Resource):
    @auth_required("token", "session")
    @api.doc(id="list_available_projects", security=["apikey"])
    def get(self):
        """List all available projects"""

        repos_resp = github.get("/user/repos")
        if not repos_resp.ok:
            print("Failed to fetch user repos.")
            return []
        repos = repos_resp.json()
        repo_names = list(map(lambda x: x["full_name"], repos))
        return repo_names
