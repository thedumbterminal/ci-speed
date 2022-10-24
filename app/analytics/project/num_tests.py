from schemas import BuildSchema
from models import Build


def _get_num_tests_for_build(build):
    build_schema = BuildSchema()
    serialised_build = build_schema.dump(build)
    result = {"x": serialised_build["created_at"], "y": 0}
    for test_run in build.test_runs:
        for test_suite in test_run.test_suites:
            result["y"] += len(test_suite.test_cases)
    return result


def get_num_tests(project_id):
    builds = Build.query.filter_by(project_id=project_id).all()
    return list(map(_get_num_tests_for_build, builds))
