import datetime as dt

class TestRunModel:
    def __init__(self, test_suites=[]):
        self.created_at = dt.datetime.now()
        self.test_suites = test_suites
