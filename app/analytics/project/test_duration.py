from schemas import BuildSchema, TestSuiteSchema as SuiteSchema
from models import Build


def get_test_duration(project_id):
    results = []

    build_schema = BuildSchema()
    test_suite_schema = SuiteSchema()
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
