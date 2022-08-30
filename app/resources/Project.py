from flask_restx import Resource, Namespace
from models import Project as ProjectModel
from schemas import ProjectSchema
from flask_security import auth_required
from analytics.project.num_tests import get_num_tests
from analytics.project.num_builds import get_num_builds
from analytics.project.test_duration import get_test_duration
from analytics.project.test_success import get_test_success
from analytics.project.tests_skipped import get_skipped_test


api = Namespace("projects", description="Project related operations")


@api.route("/<int:project_id>")
@api.param("project_id", "The project identifier")
class Project(Resource):
    @api.doc("get_project")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project"""
        project = ProjectModel.query.get(project_id)
        project_schema = ProjectSchema()
        return project_schema.dump(project)


@api.route("/<int:project_id>/num_tests")
@api.param("project_id", "The project identifier")
class ProjectNumTests(Resource):

    @api.doc("get_project test number history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's test number history"""
        return get_num_tests(project_id)


@api.route("/<int:project_id>/num_builds")
@api.param("project_id", "The project identifier")
class ProjectNumBuilds(Resource):

    @api.doc("get_project build number history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's build number history"""
        return get_num_builds(project_id)


@api.route("/<int:project_id>/test_duration")
@api.param("project_id", "The project identifier")
class ProjectTestDuration(Resource):

    @api.doc("get_project test duration history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's test duration history"""
        return get_test_duration(project_id)


@api.route("/<int:project_id>/test_success")
@api.param("project_id", "The project identifier")
class ProjectTestSuccess(Resource):

    @api.doc("get_project test success history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's test success history"""
        return get_test_success(project_id)


@api.route("/<int:project_id>/tests_skipped")
@api.param("project_id", "The project identifier")
class ProjectTestsSkipped(Resource):

    @api.doc("get_project skipped test history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's skipped test history"""
        return get_skipped_test(project_id)
