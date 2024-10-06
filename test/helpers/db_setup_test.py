import pytest
from main import app
from flask_security import login_user
from db.models import User, Build, Project
from sqlalchemy.orm.exc import NoResultFound
from db.connection import db
from models.project import find_by_name as find_project_by_name
from models.build import find_by_ref as find_build_by_ref
import uuid

test_user_email = "test@test.com"
test_project = "test_project"
test_build = "test_build"
test_waypoint = "test_waypoint"


# Setup a real db for the test user
@pytest.fixture(autouse=True, scope="session")
def setup_db():
    with app.test_request_context():
        query = User.query.filter_by(email=test_user_email)
        try:
            user = query.one()
        except NoResultFound:
            user = User(
                email=test_user_email, active=True, fs_uniquifier=uuid.uuid4().hex
            )
            db.session.add(user)
            db.session.commit()

        project = find_project_by_name(user, test_project)
        if not project:
            project = Project(test_project)
            user.projects.append(project)
            db.session.add(user)
            db.session.commit()

        build = find_build_by_ref(project, test_build)
        if not build:
            build = Build(project.id, test_build)
            db.session.add(build)
            db.session.commit()

        login_user(user)
        yield user
        db.session.delete(user)
        db.session.commit()


# this allows the above fixture to be used without having to import it
def test_setup_db():
    pass
