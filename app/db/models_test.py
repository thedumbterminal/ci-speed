from db.models import (
    TestCase as ModelTestCase,
    TestFailure as ModelTestFailure,
    SkippedTest,
)


def test_test_case_creation():
    test_case = ModelTestCase("name", 123)
    assert isinstance(test_case, ModelTestCase)


def test_test_case_creation_with_failure():
    failure = ModelTestFailure("a reason")
    test_case = ModelTestCase("name", 123, [failure])
    assert isinstance(test_case, ModelTestCase)


def test_test_case_creation_with_skipped():
    skipped = SkippedTest("another reason")
    test_case = ModelTestCase("name", 123, [], [skipped])
    assert isinstance(test_case, ModelTestCase)


def test_test_case_creation_with_failure_and_skipped():
    failure = ModelTestFailure("a reason")
    skipped = SkippedTest("another reason")
    test_case = ModelTestCase("name", 123, [failure], [skipped])
    assert isinstance(test_case, ModelTestCase)
