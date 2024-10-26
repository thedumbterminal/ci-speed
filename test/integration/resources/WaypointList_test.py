import pytest
from main import app
from db.models import User
import json
import uuid
from test.helpers.db_setup_test import test_user_email, test_project, test_build
from test.helpers.auth import (
    example_user_auth_token,
    auth_get_request,
    auth_post_request,
)


@pytest.fixture()
def example_build_id():
    with app.test_request_context():
        user = User.query.filter_by(email=test_user_email).one()
        return user.projects[0].builds[0].id


def unique_waypoint_name():
    return f"waypoint_{uuid.uuid4()}"


def test_get(example_build_id, example_user_auth_token):
    url = f"/api/waypoints/?build_id={example_build_id}"
    jData = auth_get_request(example_user_auth_token, url)
    assert type(jData) is list


def test_post_existing_build(example_build_id, example_user_auth_token):
    new_waypoint = unique_waypoint_name()
    url = "/api/waypoints/"
    data = {
        "waypoint": new_waypoint,
        "project_name": test_project,
        "build_ref": test_build,
    }
    jData = auth_post_request(example_user_auth_token, url, data)
    assert type(jData) is dict
    assert jData["name"] == new_waypoint


def test_post_unknown_build(example_build_id, example_user_auth_token):
    new_waypoint = unique_waypoint_name()
    url = "/api/waypoints/"
    data = {
        "waypoint": new_waypoint,
        "project_name": "unknown",
        "build_ref": test_build,
    }
    jData = auth_post_request(example_user_auth_token, url, data)
    assert type(jData) is dict
    assert jData["message"] == "Internal Server Error"


def test_post_new_build(example_build_id, example_user_auth_token):
    new_waypoint = unique_waypoint_name()
    url = "/api/waypoints/"
    data = {
        "waypoint": new_waypoint,
        "project_name": test_project,
        "build_ref": new_waypoint,
    }
    jData = auth_post_request(example_user_auth_token, url, data)
    assert type(jData) is dict
    assert jData["name"] == new_waypoint
