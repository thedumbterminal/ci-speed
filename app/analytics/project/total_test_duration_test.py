from app.analytics.project.total_test_duration import get_total_test_duration
import pytest
from decimal import Decimal


@pytest.fixture
def mock_function(mocker):
    return mocker.patch(
        "app.analytics.project.total_test_duration.query",
        return_value=[{"total_time": Decimal(123.456)}],
    )


def test_get_total_test_duration(mock_function):
    result = get_total_test_duration(1)
    assert result == 123.456
