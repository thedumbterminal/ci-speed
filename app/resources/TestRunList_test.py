from .TestRunList import TestRunList as ClassUnderTest
from db.models import (
    TestCase as ModelTestCase,
    TestSuite as ModelTestSuite,
    TestRun as ModelTestRun,
)
import pytest


@pytest.fixture
def resource():
    return ClassUnderTest()


def test_junit_to_test_case_success(resource):
    junit = {"@name": "a name", "@time": 123}
    test_case = resource._junit_to_test_case(junit)
    assert isinstance(test_case, ModelTestCase)


def test_junit_to_test_case_failure(resource):
    junit = {"@name": "a name", "@time": 123, "failure": "a stack trace"}
    test_case = resource._junit_to_test_case(junit)
    assert isinstance(test_case, ModelTestCase)


def test_junit_to_test_case_failure_with_message(resource):
    junit = {
        "@name": "a name",
        "@time": 123,
        "failure": {"@message": "some message", "#text": "a stack trace"},
    }
    test_case = resource._junit_to_test_case(junit)
    assert isinstance(test_case, ModelTestCase)


def test_junit_to_test_suite(resource):
    junit = {"@name": "a name", "@time": 123, "testcase": []}
    test_suite = resource._junit_to_test_suite(junit)
    assert isinstance(test_suite, ModelTestSuite)


def test_junit_to_test_run(resource):
    build_id = 1
    junit = {
        "testsuites": [
            {
                "testsuite": [
                    {
                        "@name": "test suite",
                        "@time": "1",
                        "testcase": [{"@name": "test case", "@time": "1"}],
                    }
                ]
            }
        ]
    }
    test_run = resource._junit_to_test_run(build_id, 'test-file', junit)
    assert isinstance(test_run, ModelTestRun)
