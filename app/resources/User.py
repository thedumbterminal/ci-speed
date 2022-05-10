from flask_restx import Resource, Namespace
from flask_security import auth_required, current_user
from schemas import UserSchema


api = Namespace("user", description="User related operations")

def _log_response(resp):
    print(dict(resp.headers))
    print(resp.status_code, resp.json())

@api.route("/")
class Login(Resource):
    @auth_required('session')
    @api.doc("get the info of the current user")
    def get(self):
        user_schema = UserSchema()
        return user_schema.dump(current_user)
