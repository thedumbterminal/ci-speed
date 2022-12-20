from .test_success import _get_test_success_for_build
from db.models import (
    Build,
    TestRun as ModelTestRun,
    TestSuite as ModelTestSuite,
    TestCase as ModelTestCase,
    SkippedTest,
)
from datetime import datetime
import pytest


@pytest.fixture
def empty_build():
    build = Build(1, 'test_success')
    build.created_at = datetime.fromisoformat("2011-11-04")
    return build


@pytest.fixture
def build_with_skipped_test():
    skipped_test = SkippedTest("reason")
    test_case = ModelTestCase("name", 1, [], [skipped_test])
    test_suite = ModelTestSuite("name", 1, [test_case])
    test_run = ModelTestRun(1, [test_suite])
    build = Build(1, "ref", "SHA", [test_run])
    build.created_at = datetime.fromisoformat("2011-11-04")
    return build


def test_get_test_success_for_build_with_no_test_cases(empty_build):
    result = _get_test_success_for_build(empty_build)
    assert result == {"x": "2011-11-04T00:00:00", "y": 0}
