from flask_restx import Resource, Namespace
from models import Project as ProjectModel, Build
from schemas import ProjectSchema
from flask_security import auth_required
from schemas import BuildSchema, TestSuiteSchema
from db import db


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
    def _get_num_tests(self, project_id):
        results = []

        build_schema = BuildSchema()
        builds = Build.query.filter_by(project_id=project_id).all()
        for build in builds:
            serialised_build = build_schema.dump(build)
            result = {"x": serialised_build["created_at"], "y": 0}
            for test_run in build.test_runs:
                for test_suite in test_run.test_suites:
                    result["y"] += len(test_suite.test_cases)
            results.append(result)
        return results

    @api.doc("get_project test number history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's test number history"""
        return self._get_num_tests(project_id)


@api.route("/<int:project_id>/num_builds")
@api.param("project_id", "The project identifier")
class ProjectNumBuilds(Resource):
    def _format_num_build(self, build):
        return {"x": build["date_created"].isoformat(), "y": build["num"]}

    def _get_num_builds(self, project_id):
        builds = db.session.execute(
            (
                "SELECT DATE(created_at) AS date_created, COUNT(*) AS num FROM build "
                "WHERE project_id = :project_id GROUP BY DATE(created_at);"
            ),
            {"project_id": project_id},
        )
        return list(map(self._format_num_build, builds))

    @api.doc("get_project build number history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's build number history"""
        return self._get_num_builds(project_id)


@api.route("/<int:project_id>/test_duration")
@api.param("project_id", "The project identifier")
class ProjectTestDuration(Resource):
    def _get_test_duration(self, project_id):
        results = []

        build_schema = BuildSchema()
        test_suite_schema = TestSuiteSchema()
        builds = Build.query.filter_by(project_id=project_id).all()
        for build in builds:
            serialised_build = build_schema.dump(build)
            result = {"x": serialised_build["created_at"], "y": 0}
            for test_run in build.test_runs:
                for test_suite in test_run.test_suites:
                    serialised_test_suite = test_suite_schema.dump(test_suite)
                    result["y"] += serialised_test_suite["time"]
            results.append(result)
        return results

    @api.doc("get_project test duration history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's test duration history"""
        return self._get_test_duration(project_id)


@api.route("/<int:project_id>/test_success")
@api.param("project_id", "The project identifier")
class ProjectTestSuccess(Resource):
    def _get_test_success_for_build(self, build):
        build_schema = BuildSchema()
        serialised_build = build_schema.dump(build)
        result = {"x": serialised_build["created_at"], "y": 0}
        success = 0
        fail = 0
        for test_run in build.test_runs:
            for test_suite in test_run.test_suites:
                for test_case in test_suite.test_cases:
                    if len(test_case.test_failures):
                        fail += 1
                    else:
                        success += 1
        if success > 0:
            result["y"] = (success / (fail + success)) * 100
        return result

    def _get_test_success(self, project_id):
        results = []

        builds = Build.query.filter_by(project_id=project_id).all()
        for build in builds:
            result = self._get_test_success_for_build(build)
            results.append(result)
        return results

    @api.doc("get_project test success history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's test success history"""
        return self._get_test_success(project_id)


@api.route("/<int:project_id>/tests_skipped")
@api.param("project_id", "The project identifier")
class ProjectTestsSkipped(Resource):
    def _get_skipped_test_for_build(self, build):
        build_schema = BuildSchema()
        serialised_build = build_schema.dump(build)
        result = {"x": serialised_build["created_at"], "y": 0}
        total = 0
        skipped = 0
        for test_run in build.test_runs:
            for test_suite in test_run.test_suites:
                total += len(test_suite.test_cases)
                for test_case in test_suite.test_cases:
                    if len(test_case.skipped_tests):
                        skipped += 1
        if total > 0:
            result["y"] = (skipped / total) * 100
        return result

    def _get_skipped_test(self, project_id):
        results = []

        builds = Build.query.filter_by(project_id=project_id).all()
        for build in builds:
            result = self._get_skipped_test_for_build(build)
            results.append(result)
        return results

    @api.doc("get_project skipped test history")
    @auth_required("token", "session")
    @api.doc(security=["apikey"])
    def get(self, project_id):
        """Retrieve a project's skipped test history"""
        return self._get_skipped_test(project_id)
