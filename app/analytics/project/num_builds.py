from db.query import query


def _format_num_build(build):
    return {"x": build["date_created"].isoformat(), "y": build["num"]}


def get_num_builds(project_id):
    builds = query(
        (
            "SELECT DATE(created_at) AS date_created, COUNT(*) AS num FROM build "
            "WHERE project_id = :project_id GROUP BY DATE(created_at);"
        ),
        {"project_id": project_id},
    )
    return list(map(_format_num_build, builds))
