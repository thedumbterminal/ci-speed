from flask_restx import Resource, Namespace
from schemas import ProjectSchema
from flask_security import auth_required, current_user
from analytics.project.num_tests import get_num_tests
from analytics.project.num_builds import get_num_builds
from analytics.project.test_duration import get_test_duration
from analytics.project.test_success import get_test_success
from analytics.project.tests_skipped import get_skipped_test
from analytics.project.total_test_duration import get_total_test_duration
from analytics.project.test_pass_percentage import get_test_pass_percentage
from models.project import find_by_id

api = Namespace("projects", description="Project related operations")

analytics_parser = api.parser()
analytics_parser.add_argument(
    "days", type=int, location="args", help="Duration", required=False, default=30
)


@api.route("/<int:project_id>")
@api.param("project_id", "The project identifier")
class Project(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_project", security=["apikey"])
    def get(self, project_id):
        """Retrieve a project"""
        project = find_by_id(current_user, project_id)
        project_schema = ProjectSchema()
        return project_schema.dump(project)


@api.route("/<int:project_id>/num_tests")
@api.param("project_id", "The project identifier")
class ProjectNumTests(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_project_test_number_history", security=["apikey"])
    @api.expect(analytics_parser)
    def get(self, project_id):
        """Retrieve a project's test number history"""
        args = analytics_parser.parse_args()
        return get_num_tests(project_id, args["days"])


@api.route("/<int:project_id>/num_builds")
@api.param("project_id", "The project identifier")
class ProjectNumBuilds(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_project_build_number_history", security=["apikey"])
    @api.expect(analytics_parser)
    def get(self, project_id):
        """Retrieve a project's build number history"""
        args = analytics_parser.parse_args()
        return get_num_builds(project_id, args["days"])


@api.route("/<int:project_id>/test_duration")
@api.param("project_id", "The project identifier")
class ProjectTestDuration(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_project_test_duration_history", security=["apikey"])
    @api.expect(analytics_parser)
    def get(self, project_id):
        """Retrieve a project's test duration history"""
        args = analytics_parser.parse_args()
        return get_test_duration(project_id, args["days"])


@api.route("/<int:project_id>/test_success")
@api.param("project_id", "The project identifier")
class ProjectTestSuccess(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_project_test_success_history", security=["apikey"])
    @api.expect(analytics_parser)
    def get(self, project_id):
        """Retrieve a project's test success history"""
        args = analytics_parser.parse_args()
        return get_test_success(project_id, args["days"])


@api.route("/<int:project_id>/tests_skipped")
@api.param("project_id", "The project identifier")
class ProjectTestsSkipped(Resource):
    @auth_required("token", "session")
    @api.doc(id="get_project_skipped_test_history", security=["apikey"])
    @api.expect(analytics_parser)
    def get(self, project_id):
        """Retrieve a project's skipped test history"""
        args = analytics_parser.parse_args()
        return get_skipped_test(project_id, args["days"])


@api.route("/<int:project_id>/total_test_duration")
@api.param("project_id", "The project identifier")
class TotalTestDuration(Resource):
    @auth_required("token", "session")
    @api.doc(id="get summary_total_test_duration", security=["apikey"])
    def get(self, project_id):
        """Retrieve the total test duration for a project"""
        return get_total_test_duration(project_id)


@api.route("/<int:project_id>/test_pass_percentage")
@api.param("project_id", "The project identifier")
class TestPassPercentage(Resource):
    @auth_required("token", "session")
    @api.doc(id="get test pass percentage", security=["apikey"])
    def get(self, project_id):
        """Retrieve the test pass percentage for a project"""
        return get_test_pass_percentage(project_id)
