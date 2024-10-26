import pytest
from main import app
from flask_security import login_user
from db.models import (
    User,
    Build,
    Project,
    TestRun as ModelTestRun,
    TestSuite as ModelTestSuite,
)
from sqlalchemy.orm.exc import NoResultFound
from db.connection import db
from models.project import find_by_name as find_project_by_name
from models.build import find_by_ref as find_build_by_ref
import uuid

test_user_email = "test@test.com"
test_project = "test_project"
test_build = "test_build"
test_waypoint = "test_waypoint"
test_run_file_name = "test_file_name"
test_suite_name = "test_suite"


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

        project = setup_project(user)
        build = setup_build(project)
        test_run = setup_test_run(build)
        test_suite = setup_test_suite(test_run)

        login_user(user)
        db.session.commit()
        yield user
        db.session.delete(project)
        db.session.delete(user)
        db.session.commit()


def setup_project(user):
    project = find_project_by_name(user, test_project)
    if not project:
        project = Project(test_project)
        user.projects.append(project)
        db.session.add(user)
        db.session.commit()
    return project


def setup_build(project):
    build = find_build_by_ref(project, test_build)
    if not build:
        build = Build(project.id, test_build)
        db.session.add(build)
        db.session.commit()
    return build


def setup_test_run(build):
    test_run = ModelTestRun(build.id, test_run_file_name)
    db.session.add(test_run)
    db.session.commit()
    return test_run


def setup_test_suite(test_run):
    test_suite = ModelTestSuite(test_run.id, test_suite_name, 1)
    db.session.add(test_suite)
    db.session.commit()
    return test_suite


# this allows the above fixture to be used without having to import it
def test_setup_db():
    pass
