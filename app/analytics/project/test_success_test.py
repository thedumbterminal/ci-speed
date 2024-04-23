from .test_success import get_test_success
from datetime import date
import pytest


@pytest.fixture
def mock_function(mocker):
    return mocker.patch(
        "app.analytics.project.test_success.query",
        return_value=[
            {"date_created": date.fromisoformat("2022-01-02"), "percent": 12.3}
        ],
    )


def test_get_test_success(mock_function):
    result = get_test_success(1, 1)
    assert result == [{"x": "2022-01-02", "y": 12.3}]
