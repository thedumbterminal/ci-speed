from .tests_skipped import get_skipped_test
from datetime import date
import pytest


@pytest.fixture
def mock_function(mocker):
    return mocker.patch(
        "app.analytics.project.tests_skipped.query",
        return_value=[
            {"date_created": date.fromisoformat("2022-01-02"), "percent": 12.3}
        ],
    )


def test_get_skipped_test(mock_function):
    result = get_skipped_test(1, 1)
    assert result == [{"x": "2022-01-02", "y": 12.3}]
