from db import db
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ... other columns as needed

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __init__(self, name, test_runs=[]):
        self.name = name
        self.test_runs = test_runs


class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    project = db.relationship(
        'Project',
        backref="test_runs",
        cascade="all, delete",
        passive_deletes=True
    )

    def __init__(self, project_id, test_suites=[]):
        self.project_id = project_id
        self.test_suites = test_suites


class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    time = db.Column(db.Numeric())
    test_run_id = db.Column(db.Integer, db.ForeignKey("test_run.id"))
    test_run = db.relationship(
        'TestRun',
        backref="test_suites",
        cascade="all, delete",
        passive_deletes=True
    )

    def __init__(self, name, time, test_cases=[]):
        self.name = name
        self.time = time
        self.test_cases = test_cases


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    time = db.Column(db.Numeric())
    test_suite_id = db.Column(db.Integer, db.ForeignKey("test_suite.id"))
    test_suite = db.relationship(
        'TestSuite',
        backref="test_cases",
        cascade="all, delete",
        passive_deletes=True
    )

    def __init__(self, name, time):
        self.name = name
        self.time = time
