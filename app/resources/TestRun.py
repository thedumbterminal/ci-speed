from flask_restx import Resource, Namespace, fields

from werkzeug.datastructures import FileStorage

api = Namespace("test_run", description="Test run related operations")

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@api.route("/")
class TestRun(Resource):
    @api.doc("get_test_run")
    def get(self):
        return {'hello': 'world'}

    @api.doc("post_test_run")
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        print(uploaded_file.read())
        return True

