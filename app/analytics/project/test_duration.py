from lib.date import date_in_past
from db.query import query


def _format_result(build):
    return {"x": build["date_created"].isoformat(), "y": build["total_time"]}


def get_test_duration(project_id, days):
    builds = query(
        (
            "SELECT "
            "DATE(build.created_at) AS date_created, "
            "CAST(SUM(test_suite.time) AS INTEGER) AS total_time "
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
    return list(map(_format_result, builds))
