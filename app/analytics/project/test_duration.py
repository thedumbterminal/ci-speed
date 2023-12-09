from schemas import BuildSchema, TestSuiteSchema as SuiteSchema
from db.models import Build
from sqlalchemy import and_
from lib.date import date_in_past

build_schema = BuildSchema()
test_suite_schema = SuiteSchema()


def _get_test_duration_for_build(build):
    serialised_build = build_schema.dump(build)
    result = {"x": serialised_build["created_at"], "y": 0}
    for test_run in build.test_runs:
        for test_suite in test_run.test_suites:
            serialised_test_suite = test_suite_schema.dump(test_suite)
            result["y"] += serialised_test_suite["time"]
    return result


def get_test_duration(project_id, days):
    builds = Build.query.filter(
        and_(Build.project_id == project_id, Build.created_at >= date_in_past(days))
    ).all()
    return list(map(_get_test_duration_for_build, builds))
