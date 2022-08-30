from schemas import BuildSchema
from models import Build


def get_num_tests(project_id):
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
