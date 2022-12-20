from db.connection import db


def _query(sql, values):
    return db.session.execute(sql, values)


def get_total_test_duration(project_id):
    result = _query(
        (
            "SELECT sum(test_suite.time) AS total_time "
            "FROM build "
            "LEFT JOIN test_run ON (test_run.build_id = build.id) "
            "LEFT JOIN test_suite ON (test_suite.test_run_id = test_run.id) "
            "WHERE build.project_id = :project_id;"
        ),
        {"project_id": project_id},
    )
    results_as_dict = result.mappings().all()
    return float(results_as_dict[0]["total_time"])
