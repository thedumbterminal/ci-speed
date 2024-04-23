from .test_duration import get_test_duration
from datetime import date
import pytest


@pytest.fixture
def mock_function(mocker):
    return mocker.patch(
        "app.analytics.project.test_duration.query",
        return_value=[
            {"date_created": date.fromisoformat("2022-01-02"), "total_time": 12.3}
        ],
    )


def test_get_test_duration(mock_function):
    result = get_test_duration(1, 1)
    assert result == [{"x": "2022-01-02", "y": 12.3}]
