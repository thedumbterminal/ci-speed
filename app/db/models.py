from db.connection import db
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, Security
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.ext.hybrid import hybrid_property

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


users_projects = db.Table(
    "users_projects",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), nullable=False),
    db.Column("project_id", db.Integer(), db.ForeignKey("project.id"), nullable=False),
    db.UniqueConstraint("user_id", "project_id", name="uniq_user_project"),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    db.UniqueConstraint(name, name="uniq_name")

    def __init__(self, name, builds=[]):
        self.name = name
        self.builds = builds


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship(
        Role, secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )
    projects = db.relationship(
        Project,
        secondary=users_projects,
        backref=db.backref("projects", lazy="dynamic"),
    )


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    ref = db.Column(db.String(), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    commit_sha = db.Column(db.String(), nullable=True)
    project = db.relationship(
        Project, backref="builds", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, project_id, ref, commit_sha="", test_runs=[]):
        self.project_id = project_id
        self.ref = ref
        self.commit_sha = commit_sha
        self.test_runs = test_runs

    @hybrid_property
    def commit_url(self):
        project_name = self.project.name
        return f"https://github.com/{project_name}/commit/{self.commit_sha}"


class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    build_id = db.Column(db.Integer, db.ForeignKey("build.id"), nullable=False)
    build = db.relationship(
        Build, backref="test_runs", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, build_id, test_suites=[]):
        self.build_id = build_id
        self.test_suites = test_suites


class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    time = db.Column(db.Numeric())
    test_run_id = db.Column(db.Integer, db.ForeignKey("test_run.id"), nullable=False)
    test_run = db.relationship(
        TestRun, backref="test_suites", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, name, time, test_cases=[]):
        self.name = name
        self.time = time
        self.test_cases = test_cases


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    time = db.Column(db.Numeric())
    test_suite_id = db.Column(
        db.Integer, db.ForeignKey("test_suite.id"), nullable=False
    )
    test_suite = db.relationship(
        TestSuite, backref="test_cases", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, name, time, test_failures=[], skipped_tests=[]):
        self.name = name
        self.time = time
        self.test_failures = test_failures
        self.skipped_tests = skipped_tests


class TestFailure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(), nullable=False)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)
    test_case = db.relationship(
        TestCase, backref="test_failures", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, reason):
        self.reason = reason


class SkippedTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(), nullable=False)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)
    test_case = db.relationship(
        TestCase, backref="skipped_tests", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, reason):
        self.reason = reason


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
