from .Project import ProjectTestSuccess, ProjectTestsSkipped, ProjectNumBuilds
from models import (
    Build,
    TestRun as ModelTestRun,
    TestSuite as ModelTestSuite,
    TestCase as ModelTestCase,
    SkippedTest,
)
from datetime import datetime, date
import pytest


@pytest.fixture
def empty_build():
    build = Build(1)
    build.created_at = datetime.fromisoformat("2011-11-04")
    return build


@pytest.fixture
def build_with_skipped_test():
    skipped_test = SkippedTest("reason")
    test_case = ModelTestCase("name", 1, [], [skipped_test])
    test_suite = ModelTestSuite("name", 1, [test_case])
    test_run = ModelTestRun(1, [test_suite])
    build = Build(1, "ref", [test_run])
    build.created_at = datetime.fromisoformat("2011-11-04")
    return build


def test_get_success_for_build_with_no_test_cases(empty_build):
    route = ProjectTestSuccess()
    result = route._get_test_success_for_build(empty_build)
    assert result == {"x": "2011-11-04T00:00:00", "y": 0}


def test_get_skipped_test_for_build_with_no_test_cases(empty_build):
    route = ProjectTestsSkipped()
    result = route._get_skipped_test_for_build(empty_build)
    assert result == {"x": "2011-11-04T00:00:00", "y": 0}


def test_get_skipped_test_for_build_with_skipped_test_cases(build_with_skipped_test):
    route = ProjectTestsSkipped()
    result = route._get_skipped_test_for_build(build_with_skipped_test)
    assert result == {"x": "2011-11-04T00:00:00", "y": 100}


def test_get_num_builds(mocker):
    mocker.patch.object(
        ProjectNumBuilds,
        "_query",
        return_value=[{"date_created": date.fromisoformat("2022-01-02"), "num": 123}],
    )
    route = ProjectNumBuilds()
    result = route._get_num_builds(1)
    assert result == [{"x": "2022-01-02", "y": 123}]
