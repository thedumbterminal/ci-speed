from app.analytics.project.num_builds import get_num_builds
from datetime import date
import pytest


@pytest.fixture
def mock_function(mocker):
    return mocker.patch(
        "app.analytics.project.num_builds._query",
        return_value=[{"date_created": date.fromisoformat("2022-01-02"), "num": 123}],
    )


def test_get_num_builds(mock_function):
    result = get_num_builds(1)
    assert result == [{"x": "2022-01-02", "y": 123}]
