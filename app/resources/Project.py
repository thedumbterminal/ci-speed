from flask_restx import Resource, Namespace
from models import Project as ProjectModel
from schemas import ProjectSchema
from flask_security import auth_required


api = Namespace("projects", description="Project related operations")


@api.route("/<int:id>")
@api.param("id", "The project identifier")
class Project(Resource):
    @api.doc("get_project")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, id):
        """Retrieve a project"""
        project = ProjectModel.query.get(id)
        project_schema = ProjectSchema()
        return project_schema.dump(project)
