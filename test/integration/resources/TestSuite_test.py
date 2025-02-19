import pytest
from main import app
from db.models import User
from test.helpers.db_setup_test import test_user_email
from test.helpers.auth import auth_get_request


@pytest.fixture()
def example_test_suite_id():
    with app.test_request_context():
        user = User.query.filter_by(email=test_user_email).one()
        return user.projects[0].builds[0].test_runs[0].test_suites[0].id


def test_get(example_test_suite_id, example_user_auth_token):
    url = f"/api/test_suites/{example_test_suite_id}"
    jData = auth_get_request(example_user_auth_token, url)
    assert type(jData) is dict
