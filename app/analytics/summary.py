from db import db


def _query(sql, values):
    return db.session.execute(sql, values)


def get_total_test_duration(user_id):
    result = _query(
        (
            "select sum(test_suite.time) as total_time "
            "from project "
            "left join build on (build.project_id = project.id) "
            "left join test_run on (test_run.build_id = build.id) "
            "left join test_suite on (test_suite.test_run_id = test_run.id) "
            "where user_id = :user_id;"
        ),
        {"user_id": user_id},
    )
    results_as_dict = result.mappings().all()
    return results_as_dict[0]['total_time']
