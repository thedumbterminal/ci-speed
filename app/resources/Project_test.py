from .Project import ProjectTestSuccess, ProjectTestsSkipped
from models import (
    Build,
    TestRun as ModelTestRun,
    TestSuite as ModelTestSuite,
    TestCase as ModelTestCase,
    SkippedTest,
)
from datetime import datetime


def test_get_success_for_build_with_no_test_cases():
    route = ProjectTestSuccess()
    build = Build(1)
    build.created_at = datetime.fromisoformat("2011-11-04")
    result = route._get_test_success_for_build(build)
    assert result == {"x": "2011-11-04T00:00:00", "y": 0}


def test_get_skipped_test_for_build_with_no_test_cases():
    route = ProjectTestsSkipped()
    build = Build(1)
    build.created_at = datetime.fromisoformat("2011-11-04")
    result = route._get_skipped_test_for_build(build)
    assert result == {"x": "2011-11-04T00:00:00", "y": 0}


def test_get_skipped_test_for_build_with_skipped_test_cases():
    route = ProjectTestsSkipped()
    skipped_test = SkippedTest("reason")
    test_case = ModelTestCase("name", 1, [], [skipped_test])
    test_suite = ModelTestSuite("name", 1, [test_case])
    test_run = ModelTestRun(1, [test_suite])
    build = Build(1, "ref", [test_run])
    build.created_at = datetime.fromisoformat("2011-11-04")
    result = route._get_skipped_test_for_build(build)
    assert result == {"x": "2011-11-04T00:00:00", "y": 100}
