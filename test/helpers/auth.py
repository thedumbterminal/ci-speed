import pytest
from main import app
from db.models import User
import json
from test.helpers.db_setup_test import test_user_email


@pytest.fixture()
def example_user_auth_token():
    with app.test_request_context():
        user = User.query.filter_by(email=test_user_email).one()
        return user.get_auth_token()


def auth_get_request(token, url):
    with app.test_request_context(), app.test_client() as test_client:
        response = test_client.get(
            url,
            headers={
                "Authentication-Token": token,
                "accept": "application/json",
            },
        )
        print(response)
        print(response.status_code)
        return json.loads(response.data)


def auth_post_request(token, url, data):
    with app.test_request_context(), app.test_client() as test_client:
        response = test_client.post(
            url,
            headers={
                "Authentication-Token": token,
                "accept": "application/json",
            },
            data=data,
        )
        print(response.status_code)
        return json.loads(response.data)
