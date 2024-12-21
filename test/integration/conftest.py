import pytest
from main import app
from db.models import User
from test.helpers.db_setup_test import test_user_email


@pytest.fixture()
def example_user_auth_token():
    with app.test_request_context():
        user = User.query.filter_by(email=test_user_email).one()
        return user.get_auth_token()
