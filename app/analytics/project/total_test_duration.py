from db.query import query


def get_total_test_duration(project_id):
    sql = (
        "SELECT sum(test_suite.time) AS total_time "
        "FROM build "
        "LEFT JOIN test_run ON (test_run.build_id = build.id) "
        "LEFT JOIN test_suite ON (test_suite.test_run_id = test_run.id) "
        "WHERE build.project_id = :project_id;"
    )

    results_as_dict = query(sql, {"project_id": project_id})
    return float(results_as_dict[0]["total_time"])
