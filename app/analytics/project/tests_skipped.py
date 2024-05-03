from db.query import query
from lib.date import date_in_past


def _format_result(build):
    return {"x": build["date_created"].isoformat(), "y": build["percent"]}


def get_skipped_test(project_id, days):
    builds = query(
        (
            "SELECT "
            "DATE(build.created_at) AS date_created, "
            "CASE "
            "WHEN COUNT(*) FILTER (WHERE skipped_test.test_case_id IS NOT NULL) > 0 THEN "
            "CAST("
            "((CAST(COUNT(*) FILTER (WHERE skipped_test.test_case_id IS NOT NULL) AS DECIMAL) / "
            "CAST(COUNT(*) FILTER (WHERE skipped_test.test_case_id IS NULL) AS DECIMAL)) * 100 "
            ") AS FLOAT) "
            "ELSE 0 "
            "END AS percent "
            "FROM build "
            "LEFT JOIN test_run ON (test_run.build_id = build.id) "
            "LEFT JOIN test_suite ON (test_suite.test_run_id = test_run.id) "
            "LEFT JOIN test_case ON (test_case.test_suite_id = test_suite.id) "
            "LEFT JOIN skipped_test on (test_case.id = skipped_test.test_case_id) "
            "WHERE "
            "build.project_id = :project_id "
            "AND build.created_at >= :date_in_past "
            "GROUP BY DATE(build.created_at);"
        ),
        {"project_id": project_id, "date_in_past": date_in_past(days)},
    )
    return list(map(_format_result, builds))
