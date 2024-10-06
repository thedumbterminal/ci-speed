from models.build import find_by_ref
import pytest
from db.models import Project, Build


@pytest.fixture
def mock_project():
    project = Project("test")
    project.id = 1
    build = Build(project.id, 'test')
    project.builds.append(build)
    return project


def test_find_by_ref(mock_project):
    result = find_by_ref(mock_project, "test")
    assert isinstance(result, Build)
    assert result.ref == "test"


def test_find_by_ref_not_found(mock_project):
    result = find_by_ref(mock_project, "not found")
    assert result == None
