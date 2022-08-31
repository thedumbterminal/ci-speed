from schemas import BuildSchema
from models import Build


def _get_skipped_test_for_build(build):
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


def get_skipped_test(project_id):
    results = []

    builds = Build.query.filter_by(project_id=project_id).all()
    for build in builds:
        result = _get_skipped_test_for_build(build)
        results.append(result)
    return results
