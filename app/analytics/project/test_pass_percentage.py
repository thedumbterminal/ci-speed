from db.query import query


def get_test_pass_percentage(project_id):
    sql = (
        "SELECT "
        "DATE(build.created_at) AS date_created, "
        "((CAST(COUNT(*) FILTER ( "
        "WHERE test_failure.test_case_id IS NOT NULL "
        "OR skipped_test.test_case_id IS NOT NULL) AS DECIMAL) "
        " / "
        "CAST(COUNT(*) FILTER ( "
        "WHERE test_failure.test_case_id IS NULL "
        "AND skipped_test.test_case_id IS NULL) AS DECIMAL) "
        ") * 100 "
        ") AS percent "
        "FROM build "
        "LEFT JOIN test_run ON (test_run.build_id = build.id) "
        "LEFT JOIN test_suite ON (test_suite.test_run_id = test_run.id) "
        "LEFT JOIN test_case ON (test_case.test_suite_id = test_suite.id) "
        "LEFT JOIN test_failure on (test_case.id = test_failure.test_case_id) "
        "LEFT JOIN skipped_test on (test_case.id = skipped_test.test_case_id) "
        "WHERE "
        "build.project_id = :project_id "
        "AND build.created_at >= :date_in_past "
        "GROUP BY DATE(build.created_at);"
    )

    results_as_dict = query(sql, {"project_id": project_id})
    return float(results_as_dict[0]["percentage"])
