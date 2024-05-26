from db.query import query
from db.models import TestCase as TestCaseModel


def _format_result(item):
    return TestCaseModel.query.get(item['id'])


def get_results(build_id):
    results = query(
        (
            "SELECT test_case.id "
            "FROM build "
            "LEFT JOIN test_run ON (test_run.build_id = build.id) "
            "LEFT JOIN test_suite ON (test_suite.test_run_id = test_run.id) "
            "LEFT JOIN test_case ON (test_case.test_suite_id = test_suite.id) "
            "WHERE "
            "build.id = :build_id "
            "ORDER BY test_case.time DESC "
            "LIMIT 3;"
        ),
        {"build_id": build_id},
    )
    return list(map(_format_result, results))
