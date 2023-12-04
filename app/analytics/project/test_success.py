from schemas import BuildSchema
from db.models import Build
from sqlalchemy import and_
from lib.date import date_in_past


def _get_test_success_for_build(build):
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


def get_test_success(project_id, days):
    builds = Build.query.filter(
        and_(Build.project_id == project_id, Build.created_at >= date_in_past(days))
    ).all()
    return list(map(_get_test_success_for_build, builds))
