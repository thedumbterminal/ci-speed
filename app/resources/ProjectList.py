from flask_restx import Resource, Namespace
from models import Project
from schemas import ProjectSchema
from pprint import pprint
from db import db
import os
from flask_security import auth_required, current_user


api = Namespace("projects", description="Project related operations")

create_parser = api.parser()
create_parser.add_argument(
    'name',
    required=True,
    help='Name of the project',
    location='form'
)

@api.route("/")
class ProjectList(Resource):

    def _project_url(self, project):
        default_ui_base = 'http://localhost:3000'
        ui_url_base = os.environ.get('UI_URL_BASE', default_ui_base)
        return f'{ui_url_base}/#/project/?id={project.id}'

    @api.doc("list_projects")
    @auth_required('token', 'session')
    @api.doc(security=['apikey'])
    def get(self):
        '''List all projects'''
        projects = Project.query.all()
        project_schema = ProjectSchema()
        return project_schema.dump(projects, many=True)

    @api.doc("create_project")
    @api.expect(create_parser)
    @auth_required('token', 'session')
    @api.doc(security=['apikey'])
    def post(self):
        '''Create a new project for storing test runs against'''
        args = create_parser.parse_args()

        project = Project(args['name'])
        db.session.add(project)
        db.session.commit()

        print('Schema result:')
        project_schema = ProjectSchema()
        pprint(project_schema.dump(project))
        return {
            'project_url': self._project_url(project)
        }
