from db.query import query
from lib.date import date_in_past


def _format_num_test(build):
    return {"x": build["date_created"].isoformat(), "y": build["num"]}


def get_num_tests(project_id, days):
    builds = query(
        (
            "SELECT "
            "DATE(build.created_at) AS date_created, "
            "count(test_case.id) AS num "
            "FROM build "
            "LEFT JOIN test_run ON (test_run.build_id = build.id) "
            "LEFT JOIN test_suite ON (test_suite.test_run_id = test_run.id) "
            "LEFT JOIN test_case ON (test_case.test_suite_id = test_suite.id) "
            "WHERE "
            "build.project_id = :project_id "
            "AND build.created_at >= :date_in_past "
            "GROUP BY DATE(build.created_at);"
        ),
        {"project_id": project_id, "date_in_past": date_in_past(days)},
    )
    return list(map(_format_num_test, builds))
