from flask_restx import Resource, Namespace
from models import TestCase as TestCaseModel
from schemas import TestCaseSchema

api = Namespace("test_cases", description="Test case related operations")


@api.route("/<int:id>")
@api.param('id', 'The test case identifier')
class TestCase(Resource):
    @api.doc("get_case_suite")
    def get(self, id):
        '''Retrieve a test case'''
        test_case = TestCaseModel.query.get(id)
        test_case_schema = TestCaseSchema()
        return test_case_schema.dump(test_case)
