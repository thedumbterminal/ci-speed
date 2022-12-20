from .test_duration import _get_test_duration_for_build
from db.models import Build
from datetime import datetime
import pytest


@pytest.fixture
def empty_build():
    build = Build(1, 'test_duration')
    build.created_at = datetime.fromisoformat("2011-11-04")
    return build


def test_get_test_duration_for_build_with_no_test_cases(empty_build):
    result = _get_test_duration_for_build(empty_build)
    assert result == {"x": "2011-11-04T00:00:00", "y": 0}
