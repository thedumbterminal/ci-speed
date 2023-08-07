from db.models import (
    TestCase as ModelTestCase,
    TestFailure as ModelTestFailure,
    Build,
    Project,
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


def test_build_commit_url():
    build = Build(1, "REF", "COMMIT")
    build.project = Project("PROJECT")
    assert build.commit_url == "https://github.com/PROJECT/commit/COMMIT"


def test_project_vcs_url():
    project = Project("PROJECT")
    assert project.vcs_url == "https://github.com/PROJECT"
