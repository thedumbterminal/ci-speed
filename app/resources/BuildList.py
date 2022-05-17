from flask_restx import Resource, Namespace
from models import Build
from schemas import BuildSchema
from pprint import pprint
from db import db
from flask_security import auth_required, current_user


api = Namespace("builds", description="Build related operations")

create_parser = api.parser()
create_parser.add_argument(
    'id',
    required=True,
    help='ID of the project',
    location='form'
)

@api.route("/")
class BuildList(Resource):

    @api.doc("list_builds")
    @auth_required('token', 'session')
    @api.doc(security=['apikey'])
    def get(self):
        '''List all builds'''
        builds = Build.query.all()
        build_schema = BuildSchema()
        return build_schema.dump(builds, many=True)

    @api.doc("create_build")
    @api.expect(create_parser)
    @auth_required('token', 'session')
    @api.doc(security=['apikey'])
    def post(self):
        '''Create a new build for storing test runs against'''
        args = create_parser.parse_args()

        build = Build(args['name'])
        db.session.add(project)
        db.session.commit()

        print('Schema result:')
        build_schema = BuildSchema()
        pprint(build_schema.dump(build))
        return {
            'project_url': self._project_url(build)
        }
