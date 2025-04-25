from models.project import find_by_id, find_by_name
import pytest
from db.models import User, Project


@pytest.fixture
def mock_user():
    user = User()
    project = Project("test")
    project.id = 1
    project2 = Project("test2")
    project2.id = 2
    user.projects.append(project)
    user.projects.append(project2)
    return user


def test_find_by_id(mock_user):
    result = find_by_id(mock_user, 1)
    assert isinstance(result, Project)
    assert result.id == 1


def test_find_by_id_not_found(mock_user):
    result = find_by_id(mock_user, 100)
    assert result is None


def test_find_by_name(mock_user):
    result = find_by_name(mock_user, "test2")
    assert isinstance(result, Project)
    assert result.name == "test2"


def test_find_by_name_not_found(mock_user):
    result = find_by_name(mock_user, "not found")
    assert result is None
