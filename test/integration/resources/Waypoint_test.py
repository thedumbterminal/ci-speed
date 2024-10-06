import pytest
from main import app
from db.models import User
import json
import uuid
from test.helpers.db_setup import setup_db, test_user_email, test_project, test_build


@pytest.fixture()
def example_waypoint_id():
    with app.test_request_context():
        user = User.query.filter_by(email=test_user_email).one()
        return user.projects[0].builds[0].waypoints[0].id


@pytest.fixture()
def example_user_auth_token():
    with app.test_request_context():
        user = User.query.filter_by(email=test_user_email).one()
        return user.get_auth_token()


def auth_get_request(token, url):
    with app.test_request_context(), app.test_client() as test_client:
        response = test_client.get(url,
            headers = {
                'Authentication-Token': token,
                'accept': 'application/json',
            }
        )
        print(response.status_code)
        return json.loads(response.data)


def test_get(example_waypoint_id, example_user_auth_token):
    url = f"/api/waypoints/{example_waypoint_id}"
    jData = auth_get_request(example_user_auth_token, url)
    assert type(jData) is dict
