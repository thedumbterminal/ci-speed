from .num_tests import _get_num_tests_for_build
from models import (
    Build,
    TestRun as ModelTestRun,
    TestSuite as ModelTestSuite,
    TestCase as ModelTestCase,
)
from datetime import datetime
import pytest


@pytest.fixture
def build_with_tests():
    test_case = ModelTestCase("name", 1, [], [])
    test_suite = ModelTestSuite("name", 1, [test_case])
    test_run = ModelTestRun(1, [test_suite])
    build = Build(1, "ref", [test_run])
    build.created_at = datetime.fromisoformat("2011-11-04")
    return build


def test_get_num_tests_for_build(build_with_tests):
    result = _get_num_tests_for_build(build_with_tests)
    assert result == {"x": "2011-11-04T00:00:00", "y": 1}
