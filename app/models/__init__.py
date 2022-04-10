from db import db


class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())

    def __init__(self, test_suites=[]):
        self.test_suites = test_suites


class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    time = db.Column(db.Numeric())
    test_run_id = db.Column(db.Integer, db.ForeignKey("test_run.id"))
    test_run = db.relationship('TestRun', backref="test_suites")

    def __init__(self, name, time, test_cases=[]):
        self.name = name
        self.time = time
        self.test_cases = test_cases


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    time = db.Column(db.Numeric())
    test_suite_id = db.Column(db.Integer, db.ForeignKey("test_suite.id"))
    test_suite = db.relationship('TestSuite', backref="test_cases")

    def __init__(self, name, time):
        self.name = name
        self.time = time
