from flask_restx import Resource, Namespace
from models import TestSuite as TestSuiteModel
from schemas import TestSuiteSchema

api = Namespace("test_suites", description="Test suite related operations")

@api.route("/<int:id>")
@api.param('id', 'The test suite identifier')
class TestSuite(Resource):
    @api.doc("get_test_suite")
    def get(self, id):
        '''Retrieve a test suite'''
        test_suite = TestSuiteModel.query.get(id)
        test_suite_schema = TestSuiteSchema()
        return test_suite_schema.dump(test_suite)
