import pytest
from main import app
from db.models import User
from test.helpers.db_setup_test import test_user_email
from test.helpers.auth import auth_get_request


@pytest.fixture()
def example_waypoint_id():
    with app.test_request_context():
        user = User.query.filter_by(email=test_user_email).one()
        return user.projects[0].builds[0].waypoints[0].id


def test_get(example_waypoint_id, example_user_auth_token):
    url = f"/api/waypoints/{example_waypoint_id}"
    jData = auth_get_request(example_user_auth_token, url)
    assert type(jData) is dict
