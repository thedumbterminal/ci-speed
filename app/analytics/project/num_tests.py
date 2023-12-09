from schemas import BuildSchema
from db.models import Build
from sqlalchemy import and_
from lib.date import date_in_past

build_schema = BuildSchema()


def _get_num_tests_for_build(build):
    serialised_build = build_schema.dump(build)
    result = {"x": serialised_build["created_at"], "y": 0}
    for test_run in build.test_runs:
        for test_suite in test_run.test_suites:
            result["y"] += len(test_suite.test_cases)
    return result


def get_num_tests(project_id, days):
    builds = Build.query.filter(
        and_(Build.project_id == project_id, Build.created_at >= date_in_past(days))
    ).all()
    return list(map(_get_num_tests_for_build, builds))
