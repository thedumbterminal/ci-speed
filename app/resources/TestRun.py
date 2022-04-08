from flask_restx import Resource, Namespace
from models import TestRun as TestRunModel
from schemas import TestRunSchema

api = Namespace("test_runs", description="Test run related operations")

@api.route("/<int:id>")
@api.param('id', 'The test run identifier')
class TestRun(Resource):
    @api.doc("get_test_run")
    def get(self, id):
        '''Retrieve a test run'''
        test_run = TestRunModel.query.get(id)
        test_run_schema = TestRunSchema()
        return test_run_schema.dump(test_run)
