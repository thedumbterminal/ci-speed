from .TestRunList import TestRunList as ClassUnderTest
import pytest


@pytest.mark.skip(reason="Not finished")
def test_junit_to_test_run():
    build_id = 1
    junit = {}
    testRunList = ClassUnderTest()
    test_run = testRunList._junit_to_test_run(build_id, junit)
    assert test_run
