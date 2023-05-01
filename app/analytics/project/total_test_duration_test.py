from app.analytics.project.total_test_duration import get_total_test_duration
import pytest
from decimal import Decimal


@pytest.fixture
def mock_function(mocker):
    mocked_cursor_result = mocker.MagicMock()
    mocked_cursor_result.mappings.return_value = mocker.MagicMock()
    mocked_cursor_result.mappings.return_value.all.return_value = [
        {"total_time": Decimal(123.456)}
    ]
    return mocker.patch(
        "app.analytics.project.total_test_duration.db.session.execute",
        return_value=mocked_cursor_result,
    )


def test_get_total_test_duration(mock_function):
    result = get_total_test_duration(1)
    assert result == 123.456
