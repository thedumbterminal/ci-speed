import pytest
from main import app
from db.models import User
import json
import uuid
from datetime import datetime
from test.helpers.db_setup import setup_db, test_user_email, test_project, test_build


@pytest.fixture()
def example_build_id():
    with app.test_request_context():
        user = User.query.filter_by(email=test_user_email).one()
        return user.projects[0].builds[0].id


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

def auth_post_request(token, url, data):
    with app.test_request_context(), app.test_client() as test_client:
        response = test_client.post(url,
            headers = {
                'Authentication-Token': token,
                'accept': 'application/json',
            },
            data = data
        )
        print(response.status_code)
        return json.loads(response.data)

def unique_waypoint_name():
    date = datetime.now()
    return f"waypoint_{date}"


def test_get(example_build_id, example_user_auth_token):
    url = f"/api/waypoints/?build_id={example_build_id}"
    jData = auth_get_request(example_user_auth_token, url)
    assert type(jData) is list


def test_post_existing_build(example_build_id, example_user_auth_token):
    new_waypoint = unique_waypoint_name()
    url = f"/api/waypoints/"
    data = {
        "waypoint": new_waypoint,
        "project_name": test_project,
        "build_ref": test_build
    }
    jData = auth_post_request(example_user_auth_token, url, data)
    assert type(jData) is dict
    assert jData['name'] == new_waypoint


def test_post_unknown_build(example_build_id, example_user_auth_token):
    new_waypoint = unique_waypoint_name()
    url = f"/api/waypoints/"
    data = {
        "waypoint": new_waypoint,
        "project_name": "unknown",
        "build_ref": test_build
    }
    jData = auth_post_request(example_user_auth_token, url, data)
    assert type(jData) is dict
    assert jData['message'] == 'Internal Server Error'


def test_post_new_build(example_build_id, example_user_auth_token):
    new_waypoint = unique_waypoint_name()
    url = f"/api/waypoints/"
    data = {
        "waypoint": new_waypoint,
        "project_name": test_project,
        "build_ref": new_waypoint
    }
    jData = auth_post_request(example_user_auth_token, url, data)
    assert type(jData) is dict
    assert jData['name'] == new_waypoint
