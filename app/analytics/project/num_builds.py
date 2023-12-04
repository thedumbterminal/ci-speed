from db.query import query
from lib.date import date_in_past


def _format_num_build(build):
    return {"x": build["date_created"].isoformat(), "y": build["num"]}


def get_num_builds(project_id, days):
    builds = query(
        (
            "SELECT DATE(created_at) AS date_created, COUNT(*) AS num FROM build "
            "WHERE project_id = :project_id "
            "AND created_at >= :date_in_past "
            "GROUP BY DATE(created_at);"
        ),
        {"project_id": project_id, "date_in_past": date_in_past(days)},
    )
    return list(map(_format_num_build, builds))
