from .Project import ProjectTestSuccess
from models import Build
from datetime import datetime


def test_get_success_for_build_with_no_test_cases():
    route = ProjectTestSuccess()
    build = Build(1)
    build.created_at = datetime.fromisoformat("2011-11-04")
    result = route._get_test_success_for_build(build)
    assert result == {"x": "2011-11-04T00:00:00", "y": 0}
