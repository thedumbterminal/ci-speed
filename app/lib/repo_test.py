from lib.repo import repo_list
import pytest


@pytest.fixture
def mock_function(mocker):
    return mocker.patch(
        "lib.repo._wrapped_get",
        return_value=[{"full_name": "test1"}],
    )


def test_repo_list(mock_function):
    names = repo_list()
    assert names == ["test1"]
