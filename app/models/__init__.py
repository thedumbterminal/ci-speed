from db import db
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, Security
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


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


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship(
        User, backref="projects", cascade="all, delete", passive_deletes=True
    )
    db.UniqueConstraint(user_id, name, name="uniq_user_id_project")

    def __init__(self, user_id, name, builds=[]):
        self.user_id = user_id
        self.name = name
        self.builds = builds


class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    ref = db.Column(db.String(), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    project = db.relationship(
        Project, backref="builds", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, project_id, ref="", test_runs=[]):
        self.project_id = project_id
        self.ref = ref
        self.test_runs = test_runs


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
    test_run_id = db.Column(db.Integer, db.ForeignKey("test_run.id"))
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
    test_suite_id = db.Column(db.Integer, db.ForeignKey("test_suite.id"))
    test_suite = db.relationship(
        TestSuite, backref="test_cases", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, name, time):
        self.name = name
        self.time = time


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
